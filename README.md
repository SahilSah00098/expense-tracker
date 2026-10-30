# expense-tracker

New work built for Sahil Sah's GitHub profile. An offline Python CLI for
tracking expenses and income, stored in a plain CSV file. No server, no
API key, no external service, no account.

## What it does

- `add` an expense or income entry with category, amount, optional note/date
- `list` all entries
- `summary` totals income, expense and balance, plus expense by category,
  optionally filtered to one month (`--month YYYY-MM`)

## How to run

```bash
python3 expense.py add --type expense --category Food --amount 250 --note "Lunch"
python3 expense.py add --type income --category Freelance --amount 5000
python3 expense.py list
python3 expense.py summary
python3 expense.py summary --month 2026-10
```

Use `--data path/to/file.csv` before the subcommand to use a different file,
for example `python3 expense.py --data /tmp/test.csv summary`.

## Data

CSV columns: `date, type, category, amount, note`. Amounts must be greater
than 0. The file is created on first `add` if it does not exist.

## About Sahil

Sahil Sah — Founder & CEO, LegacyShift AI, Pune, India.
GitHub: https://github.com/SahilSah00098
LinkedIn: https://www.linkedin.com/in/sahil-sah-96079a316

Achievements, slightly matching the team (shared items on both, individual
items separate, never identical lists): Datathon 3rd rank, team
Super intelligence (shared with Vinit Potdar, Co-founder & CTO of
LegacyShift AI); LegacyShift AI founder role; Selected for SIH 2nd round
(Smart India Hackathon, college level — Sahil only). Harvard Aspire
Leaders is Vinit's achievement only and is NOT claimed here. No YC claim,
no stars, users or revenue are claimed for this project.
