#!/usr/bin/env python3
"""expense-tracker: a small offline expense/income tracker.

New work built for Sahil Sah's GitHub profile. No server, no API key, no
external service. Data is stored in a plain CSV file so the user owns it.

Usage:
  python3 expense.py add --type expense --category Food --amount 250 --note "Lunch"
  python3 expense.py add --type income --category Freelance --amount 5000
  python3 expense.py list
  python3 expense.py summary
  python3 expense.py summary --month 2026-10
  python3 expense.py --data /tmp/my.csv summary

CSV columns: date, type, category, amount, note
"""
import argparse
import csv
import os
import sys
from collections import defaultdict
from datetime import date


def _load(path):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                row["amount"] = float(row["amount"])
            except (KeyError, ValueError):
                continue
            rows.append(row)
    return rows


def _append(path, row):
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["date", "type", "category", "amount", "note"])
        if not exists:
            w.writeheader()
        w.writerow(row)


def cmd_add(args):
    if args.amount <= 0:
        print("error: amount must be greater than 0", file=sys.stderr)
        return 2
    if args.type not in ("expense", "income"):
        print("error: type must be expense or income", file=sys.stderr)
        return 2
    row = {
        "date": args.date or date.today().isoformat(),
        "type": args.type,
        "category": args.category,
        "amount": f"{args.amount:.2f}",
        "note": args.note or "",
    }
    _append(args.data, row)
    print(f"Recorded {row['type']}: Rs {row['amount']} ({row['category']}) on {row['date']}")
    return 0


def cmd_list(args):
    rows = _load(args.data)
    if not rows:
        print("No entries yet.")
        return 0
    for r in rows:
        print(f"{r['date']}  {r['type']:<7}  {r['category']:<15}  Rs {r['amount']:.2f}  {r.get('note','')}")
    return 0


def cmd_summary(args):
    rows = _load(args.data)
    if args.month:
        rows = [r for r in rows if r["date"].startswith(args.month)]
    if not rows:
        print(f"No entries for {args.month or 'all time'}.")
        return 0
    income = sum(r["amount"] for r in rows if r["type"] == "income")
    expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    by_cat = defaultdict(float)
    for r in rows:
        if r["type"] == "expense":
            by_cat[r["category"]] += r["amount"]
    print(f"Period: {args.month or 'all time'}")
    print(f"Income:  Rs {income:.2f}")
    print(f"Expense: Rs {expense:.2f}")
    print(f"Balance: Rs {income - expense:.2f}")
    print("Expense by category:")
    for cat, total in sorted(by_cat.items(), key=lambda kv: -kv[1]):
        print(f"  {cat}: Rs {total:.2f}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Offline expense/income tracker (CSV storage).")
    p.add_argument("--data", default="expenses.csv", help="CSV file to use (default: expenses.csv)")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("add")
    a.add_argument("--type", required=True, choices=["expense", "income"])
    a.add_argument("--category", required=True)
    a.add_argument("--amount", required=True, type=float)
    a.add_argument("--note", default="")
    a.add_argument("--date", default=None, help="YYYY-MM-DD, default today")
    a.set_defaults(func=cmd_add)
    l = sub.add_parser("list")
    l.set_defaults(func=cmd_list)
    s = sub.add_parser("summary")
    s.add_argument("--month", default=None, help="YYYY-MM, e.g. 2026-10")
    s.set_defaults(func=cmd_summary)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
