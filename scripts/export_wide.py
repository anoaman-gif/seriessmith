#!/usr/bin/env python3
"""Export a product's data.csv into the wide series layout that data vendors deliver.

Data platforms such as CEIC's CDMNext hand customers a workbook, not a tidy
table: one column per series, dates down the side, and a separate index of
series metadata (name, unit, frequency, source). This script produces that
layout from a validated product folder so the same verified data can be
consumed the way incumbent customers consume it.

Usage:
    python3 scripts/export_wide.py outputs/<release-slug>

Reads  outputs/<release-slug>/data.csv
Writes outputs/<release-slug>/<release-slug>_series.xlsx with sheets:
    Series_Index  one row per series with its metadata
    Levels        periods x series matrix of published levels (value)
    YoY_pct       periods x series matrix of year-on-year percent changes
    MoM_pct       periods x series matrix of month-on-month percent changes
Sheets with no data are omitted. Requires openpyxl.
"""
import csv
import sys
from collections import OrderedDict
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: export_wide.py <product-folder>")
        return 2
    folder = Path(sys.argv[1])
    rows = list(csv.DictReader(open(folder / "data.csv", encoding="utf-8")))
    if not rows:
        print("no data rows")
        return 1

    from openpyxl import Workbook

    # Series key: indicator_id + geography (urban/rural splits are distinct series)
    series = OrderedDict()
    periods = set()
    for r in rows:
        key = (r["indicator_id"], r["geography"])
        s = series.setdefault(key, {
            "indicator_id": r["indicator_id"], "indicator_name": r["indicator_name"],
            "category": r["category"], "geography": r["geography"],
            "frequency": r["frequency"], "unit": r["unit"],
            "source_publisher": r["source_publisher"], "source_title": r["source_title"],
            "source_date": r["source_date"], "obs": {}})
        s["obs"][r["period"]] = r
        if not s["unit"] and r["unit"]:
            s["unit"] = r["unit"]
        periods.add(r["period"])
    periods = sorted(periods)

    wb = Workbook()
    idx = wb.active
    idx.title = "Series_Index"
    idx.append(["Series ID", "Indicator", "Category", "Geography", "Unit", "Frequency",
                "Source Publisher", "Source Release", "Source Date", "Observations",
                "First Period", "Last Period"])
    for (iid, geo), s in series.items():
        obs_periods = sorted(s["obs"])
        idx.append([iid, s["indicator_name"], s["category"], geo, s["unit"], s["frequency"],
                    s["source_publisher"], s["source_title"], s["source_date"],
                    len(obs_periods), obs_periods[0], obs_periods[-1]])

    def matrix(sheet_name, field):
        data = {}
        for (iid, geo), s in series.items():
            col = {}
            for p, r in s["obs"].items():
                v = (r.get(field) or "").strip()
                if v:
                    try:
                        col[p] = float(v)
                    except ValueError:
                        col[p] = v
            if col:
                data[(iid, geo)] = (s, col)
        if not data:
            return
        ws = wb.create_sheet(sheet_name)
        keys = list(data)
        ws.append(["Series ID"] + [k[0] for k in keys])
        ws.append(["Indicator"] + [data[k][0]["indicator_name"] for k in keys])
        ws.append(["Geography"] + [k[1] for k in keys])
        ws.append(["Unit"] + [data[k][0]["unit"] for k in keys])
        ws.append(["Period \\ Series"] + [""] * len(keys))
        for p in periods:
            ws.append([p] + [data[k][1].get(p, "") for k in keys])

    matrix("Levels", "value")
    matrix("YoY_pct", "yoy_pct")
    matrix("MoM_pct", "mom_pct")

    out = folder / f"{folder.name}_series.xlsx"
    wb.save(out)
    print(f"wrote {out} ({len(series)} series, {len(periods)} periods)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
