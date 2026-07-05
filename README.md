# CSV Report Automator

A Python script that cleans messy CSV data and generates a clear, readable summary report — automatically.

## The problem it solves

Businesses often export data from tools like Shopify, Google Forms, or a CRM, but the exports are messy: inconsistent formatting, missing values, duplicate rows. This tool cleans the data and produces a Markdown report with key statistics in seconds, ready to share with a team or client.

## What it does

- Removes empty and duplicate rows
- Calculates fill rate, unique values, and top values for every column
- Automatically detects numeric columns and computes min / max / average / sum
- Outputs a clean Markdown report and (optionally) the cleaned CSV

## Usage

```bash
python report_automator.py input.csv --output report.md --clean-csv cleaned.csv
```

## Example

See `sample_sales_data.csv` (raw, messy input) and `sample_report.md` (the generated output) in this folder for a real example.

## Tech

Pure Python standard library  no dependencies to install.

## Author

Joness Tadjo — jonesstadjo@gmail.com
