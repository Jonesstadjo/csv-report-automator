#!/usr/bin/env python3
"""
CSV Report Automator
---------------------
Automatically cleans messy CSV data and generates a clear summary report.

Real-world use case: businesses often export raw data (sales, leads, inventory)
from tools like Shopify, Google Forms, or CRMs, but the exports are messy —
inconsistent formatting, missing values, duplicate rows. This tool cleans the
data and produces a readable Markdown report with key statistics, ready to
share with a team or client.

Usage:
    python report_automator.py input.csv --output report.md
"""

import argparse
import csv
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def load_csv(filepath):
    """Load CSV into a list of dicts, handling common encoding issues."""
    try:
        with open(filepath, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]
            return rows, reader.fieldnames
    except FileNotFoundError:
        sys.exit(f"Error: file '{filepath}' not found.")
    except Exception as e:
        sys.exit(f"Error reading CSV: {e}")


def clean_data(rows):
    """Remove empty rows, strip whitespace, drop exact duplicates."""
    cleaned = []
    seen = set()
    empty_count = 0
    duplicate_count = 0

    for row in rows:
        stripped = {k: (v.strip() if v else "") for k, v in row.items()}

        if all(v == "" for v in stripped.values()):
            empty_count += 1
            continue

        row_key = tuple(stripped.items())
        if row_key in seen:
            duplicate_count += 1
            continue
        seen.add(row_key)
        cleaned.append(stripped)

    return cleaned, empty_count, duplicate_count


def analyze_column(rows, column):
    """Return basic stats for a column: fill rate, unique values, top values."""
    values = [row.get(column, "") for row in rows]
    non_empty = [v for v in values if v]
    fill_rate = len(non_empty) / len(values) * 100 if values else 0

    counter = Counter(non_empty)
    top_values = counter.most_common(5)

    numeric_values = []
    for v in non_empty:
        try:
            numeric_values.append(float(v.replace(",", "")))
        except ValueError:
            pass

    stats = {
        "fill_rate": round(fill_rate, 1),
        "unique_count": len(counter),
        "top_values": top_values,
        "is_numeric": len(numeric_values) == len(non_empty) and len(numeric_values) > 0,
    }

    if stats["is_numeric"]:
        stats["min"] = round(min(numeric_values), 2)
        stats["max"] = round(max(numeric_values), 2)
        stats["avg"] = round(sum(numeric_values) / len(numeric_values), 2)
        stats["sum"] = round(sum(numeric_values), 2)

    return stats


def generate_report(rows, fieldnames, empty_count, duplicate_count, source_file):
    """Build a Markdown report string from the analysis."""
    lines = []
    lines.append(f"# Data Report: {Path(source_file).name}")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    lines.append("## Summary")
    lines.append(f"- **Total clean rows:** {len(rows)}")
    lines.append(f"- **Empty rows removed:** {empty_count}")
    lines.append(f"- **Duplicate rows removed:** {duplicate_count}")
    lines.append(f"- **Columns:** {len(fieldnames)}\n")

    lines.append("## Column Analysis\n")
    for col in fieldnames:
        stats = analyze_column(rows, col)
        lines.append(f"### {col}")
        lines.append(f"- Fill rate: {stats['fill_rate']}%")
        lines.append(f"- Unique values: {stats['unique_count']}")

        if stats["is_numeric"]:
            lines.append(f"- Min: {stats['min']} | Max: {stats['max']} | Average: {stats['avg']} | Sum: {stats['sum']}")
        else:
            top = ", ".join(f"{val} ({count})" for val, count in stats["top_values"])
            lines.append(f"- Most common: {top}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Clean a CSV file and generate a summary report.")
    parser.add_argument("input", help="Path to the input CSV file")
    parser.add_argument("--output", default="report.md", help="Path for the output report (default: report.md)")
    parser.add_argument("--clean-csv", help="Optional: also save the cleaned CSV to this path")
    args = parser.parse_args()

    rows, fieldnames = load_csv(args.input)
    if not fieldnames:
        sys.exit("Error: CSV has no columns.")

    cleaned_rows, empty_count, duplicate_count = clean_data(rows)
    report = generate_report(cleaned_rows, fieldnames, empty_count, duplicate_count, args.input)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report saved to {args.output}")

    if args.clean_csv:
        with open(args.clean_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_rows)
        print(f"Cleaned CSV saved to {args.clean_csv}")


if __name__ == "__main__":
    main()
