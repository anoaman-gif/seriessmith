#!/usr/bin/env python3
"""Validate an SeriesSmith data product against the schema.

Usage:
    python3 scripts/validate_product.py outputs/<release-slug>

Checks performed:
  1. The product folder contains data.csv, report.md, and audit.md.
  2. data.csv has exactly the schema columns, in the schema order.
  3. Required columns are non-empty on every row.
  4. Numeric fields (value, yoy_pct, mom_pct) parse as numbers when present,
     and every row carries at least one of the three.
  5. Every data row has a matching audit entry in audit.md, matched on
     indicator_id and period.

Standard library only. Exit code 0 means PASS, 1 means FAIL.
"""

import csv
import os
import sys

# The schema, exactly as defined in schema/product_schema.md.
EXPECTED_COLUMNS = [
    "indicator_id",
    "indicator_name",
    "category",
    "geography",
    "period",
    "frequency",
    "value",
    "unit",
    "yoy_pct",
    "mom_pct",
    "source_publisher",
    "source_title",
    "source_date",
    "notes",
]

# Columns that must be non-empty on every row. value, yoy_pct, mom_pct and
# notes are handled separately: a row may legitimately carry only a published
# growth rate (value empty) or only a level (changes empty), and notes are
# optional by design.
REQUIRED_COLUMNS = [
    "indicator_id",
    "indicator_name",
    "category",
    "geography",
    "period",
    "frequency",
    "source_publisher",
    "source_title",
    "source_date",
]

NUMERIC_COLUMNS = ["value", "yoy_pct", "mom_pct"]

VALID_CATEGORIES = {
    "National Accounts",
    "Prices",
    "Industry",
    "Trade",
    "Investment",
    "Consumption",
    "Energy",
    "Employment",
    "Finance",
}

VALID_FREQUENCIES = {"Monthly", "Quarterly", "Annual"}


def parse_number(text):
    """Return the float value of a CSV numeric field.

    Accepts a leading minus sign and a decimal point. Thousands separators
    and percent signs are schema violations, so they are treated as errors
    rather than silently cleaned up.
    """
    return float(text)


def load_audit_keys(audit_path):
    """Extract (indicator_id, period) pairs attested in audit.md.

    Audit rows are Markdown table rows, so matching is done on line text:
    a data row counts as audited when some audit line contains both its
    indicator_id and its period.
    """
    lines = []
    with open(audit_path, encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith("|"):
                lines.append(line)
    return lines


def audit_covers(audit_lines, indicator_id, period):
    """True when some audit line mentions both the indicator and the period."""
    for line in audit_lines:
        if indicator_id in line and period in line:
            return True
    return False


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 scripts/validate_product.py <product-folder>")
        return 1

    folder = argv[1]
    errors = []
    warnings = []

    data_path = os.path.join(folder, "data.csv")
    report_path = os.path.join(folder, "report.md")
    audit_path = os.path.join(folder, "audit.md")

    # Check 1: required files exist.
    for path, label in [
        (data_path, "data.csv"),
        (report_path, "report.md"),
        (audit_path, "audit.md"),
    ]:
        if not os.path.isfile(path):
            errors.append(f"Missing required file: {label}")

    if errors:
        return summarize(folder, 0, errors, warnings)

    # Load audit lines once; used by the coverage check below.
    audit_lines = load_audit_keys(audit_path)

    # Checks 2 to 5 operate on data.csv.
    with open(data_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []

        # Check 2: exact schema columns, in order.
        if header != EXPECTED_COLUMNS:
            errors.append(
                "data.csv header does not match the schema.\n"
                f"  expected: {EXPECTED_COLUMNS}\n"
                f"  found:    {header}"
            )
            return summarize(folder, 0, errors, warnings)

        rows = list(reader)

    audited_rows = 0
    for index, row in enumerate(rows, start=1):
        where = f"row {index} ({row['indicator_id']}, {row['period']})"

        # Check 3: required columns are non-empty.
        for column in REQUIRED_COLUMNS:
            if not row[column] or not row[column].strip():
                errors.append(f"{where}: required column '{column}' is empty")

        # Category and frequency vocabularies, per the schema.
        if row["category"] and row["category"] not in VALID_CATEGORIES:
            errors.append(
                f"{where}: category '{row['category']}' is not in the schema list"
            )
        if row["frequency"] and row["frequency"] not in VALID_FREQUENCIES:
            errors.append(
                f"{where}: frequency '{row['frequency']}' is not Monthly, "
                "Quarterly, or Annual"
            )

        # Check 4: numeric fields parse, and the row carries at least one
        # numeric figure (a level or a published change).
        present_numbers = 0
        for column in NUMERIC_COLUMNS:
            text = (row[column] or "").strip()
            if text:
                present_numbers += 1
                try:
                    parse_number(text)
                except ValueError:
                    errors.append(
                        f"{where}: '{column}' value '{text}' is not a clean number"
                    )
        if present_numbers == 0:
            errors.append(
                f"{where}: row carries no value, yoy_pct, or mom_pct at all"
            )

        # A row with a level but no unit is a schema violation; a row with
        # only changes legitimately has an empty unit.
        if (row["value"] or "").strip() and not (row["unit"] or "").strip():
            errors.append(f"{where}: value is present but unit is empty")

        # Check 5: audit coverage.
        if audit_covers(audit_lines, row["indicator_id"], row["period"]):
            audited_rows += 1
        else:
            errors.append(f"{where}: no matching entry in audit.md")

    # Check 6: row identity is unique. A series is identified by
    # (indicator_id, geography, period): the same indicator may legitimately
    # appear for several geographies in one period (urban and rural splits),
    # but the same triple twice is a duplicate, not a series.
    seen = {}
    for index, row in enumerate(rows, start=1):
        key = (row["indicator_id"], row["geography"], row["period"])
        if key in seen:
            errors.append(
                f"row {index}: duplicate series key {key}, first seen at row {seen[key]}"
            )
        else:
            seen[key] = index

    # Check 7 (warning only): series identity is governed by the registry.
    # Pre-registry products and new countries legitimately contain series the
    # registry has not absorbed yet, so unregistered IDs are surfaced as a
    # warning count, never silently passed over and never a hard failure.
    registry_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "schema", "series_registry.csv",
    )
    if os.path.isfile(registry_path):
        registered = set()
        with open(registry_path, encoding="utf-8") as handle:
            for entry in csv.DictReader(handle):
                registered.add(entry["indicator_id"])
                for variant in (entry.get("variant_ids_seen") or "").split(";"):
                    if variant.strip():
                        registered.add(variant.strip())
        unregistered = sorted({row["indicator_id"] for row in rows} - registered)
        if unregistered:
            warnings.append(
                f"{len(unregistered)} indicator_id(s) are not in the series registry "
                f"yet (first: {unregistered[0]}). Register them so identity stays governed."
            )

    return summarize(folder, len(rows), errors, warnings, audited_rows)


def summarize(folder, row_count, errors, warnings, audited_rows=None):
    """Print the PASS/FAIL summary and return the process exit code."""
    print(f"Product folder: {folder}")
    print(f"Data rows checked: {row_count}")
    if audited_rows is not None:
        print(f"Rows with a matching audit entry: {audited_rows}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"\nFAIL: {len(errors)} problem(s) found:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("\nPASS: product conforms to the schema and every row is audited.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
