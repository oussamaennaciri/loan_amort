# loan_amort/cli.py

import argparse
import sys
import datetime
import matplotlib

from loan_amort.amort import amortize_loan
from loan_amort.metrics import compute_loan_metrics
from loan_amort.plots import (
    plot_balance_line,
    plot_interest_principal_line,
    plot_interest_principal_stacked,
    plot_cumulative_line,
)

def add_common_args(p):
    p.add_argument("-P", "--principal", type=float, required=True,
                   help="Loan principal (e.g. 250000)")
    p.add_argument("-r", "--rate", type=float, required=True,
                   help="Annual rate as decimal (e.g. 0.05)")
    p.add_argument("-y", "--years", type=int, required=True,
                   help="Term in years (e.g. 30)")
    p.add_argument("-k", "--per-year", type=int, default=12,
                   help="Payments per year (default: 12)")
    p.add_argument("--first-date", type=str,
                   help="Date of first payment (YYYY-MM-DD)")

def cmd_amortize(args):
    first_date = None
    if args.first_date:
        first_date = datetime.datetime.strptime(args.first_date, "%Y-%m-%d").date()

    schedule = amortize_loan(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        payments_per_year=args.per_year,
        first_payment_date=first_date
    )

    # Header
    header = f"{'Period':>6} "
    if first_date:
        header += f"{'Date':>12} "
    header += f"{'Payment':>10} {'Interest':>10} {'Principal':>10} {'Balance':>12}"
    print(header)

    # Rows
    for p in schedule:
        line = f"{p['period']:6d} "
        if first_date:
            line += f"{p['date']:12s} "
        line += (f"{p['payment']:10.2f} {p['interest']:10.2f} "
                 f"{p['principal']:10.2f} {p['balance']:12.2f}")
        print(line)

def cmd_metrics(args):
    first_date = None
    if args.first_date:
        first_date = datetime.datetime.strptime(args.first_date, "%Y-%m-%d").date()

    schedule = amortize_loan(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        payments_per_year=args.per_year,
        first_payment_date=first_date
    )
    m = compute_loan_metrics(schedule)
    for k, v in m.items():
        print(f"{k:15s}: {v}")

def cmd_plot(args):
    first_date = None
    if args.first_date:
        first_date = datetime.datetime.strptime(args.first_date, "%Y-%m-%d").date()

    schedule = amortize_loan(
        principal=args.principal,
        annual_rate=args.rate,
        years=args.years,
        payments_per_year=args.per_year,
        first_payment_date=first_date
    )

    key = args.which
    if key == "balance_line":
        fig = plot_balance_line(schedule)
    elif key == "interest_line":
        fig = plot_interest_principal_line(schedule)
    elif key == "interest_stacked":
        fig = plot_interest_principal_stacked(schedule)
    elif key == "cumulative_line":
        fig = plot_cumulative_line(schedule)
    else:
        print("Unknown plot type:", key, file=sys.stderr)
        sys.exit(1)

    # Show or save
    if matplotlib.get_backend().lower() == "agg":
        defaults = {
            "balance_line":   "balance_line.png",
            "interest_line":  "interest_line.png",
            "interest_stacked":"interest_stacked.png",
            "cumulative_line":"cumulative_line.png",
        }
        default_fn = defaults[key]
        fn = input(f"No GUI detected: save plot to file? [{default_fn}] ").strip() or default_fn
        fig.savefig(fn)
        print(f"Saved plot to {fn}")
    else:
        fig.show()

def cmd_interactive(args):
    # Gather inputs once
    principal = float(input("What is the loan principal? "))
    rate = float(input("What is the annual interest rate (decimal, e.g. 0.05)? "))
    years = int(input("What is the term in years? "))
    per_year = input("Payments per year [12]? ").strip()
    payments_per_year = int(per_year) if per_year else 12
    first_date_str = input("What is the date of the first payment? (YYYY-MM-DD)? ").strip()
    first_date = datetime.datetime.strptime(first_date_str, "%Y-%m-%d").date()

    # Precompute schedule
    schedule = amortize_loan(
        principal,
        rate,
        years,
        payments_per_year,
        first_payment_date=first_date
    )

    # Loop menu
    while True:
        print("""
What would you like to do?
  1) Print amortization schedule
  2) Show summary metrics
  3) Plot schedule components
  4) Exit
""")
        choice = input("Enter 1, 2, 3 or 4: ").strip()

        if choice == "1":
            cmd_amortize(argparse.Namespace(
                principal=principal, rate=rate, years=years,
                per_year=payments_per_year, first_date=first_date_str
            ))

        elif choice == "2":
            cmd_metrics(argparse.Namespace(
                principal=principal, rate=rate, years=years,
                per_year=payments_per_year, first_date=first_date_str
            ))

        elif choice == "3":
            print("""
Which plot would you like?
  1) Balance (line)
  2) Interest vs principal (line)
  3) Interest vs principal (stacked)
  4) Cumulative interest vs principal (line)
""")
            sel = input("Enter 1-4: ").strip()
            mapping = {
                "1": "balance_line",
                "2": "interest_line",
                "3": "interest_stacked",
                "4": "cumulative_line",
            }
            key = mapping.get(sel)
            if not key:
                print("Invalid plot choice.")
                continue
            cmd_plot(argparse.Namespace(
                principal=principal, rate=rate, years=years,
                per_year=payments_per_year, first_date=first_date_str,
                which=key
            ))

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice—please enter 1, 2, 3 or 4.")

def main():
    parser = argparse.ArgumentParser(prog="loan_amort")
    parser.set_defaults(func=cmd_interactive)
    sub = parser.add_subparsers(dest="cmd")

    p_am = sub.add_parser("amortize", help="Print full amortization schedule")
    add_common_args(p_am)
    p_am.set_defaults(func=cmd_amortize)

    p_me = sub.add_parser("metrics", help="Print loan summary metrics")
    add_common_args(p_me)
    p_me.set_defaults(func=cmd_metrics)

    p_pl = sub.add_parser("plot", help="Plot schedule components")
    add_common_args(p_pl)
    p_pl.add_argument("which", choices=[
        "balance_line",
        "interest_line",
        "interest_stacked",
        "cumulative_line",
    ], help="Which plot to draw")
    p_pl.set_defaults(func=cmd_plot)

    p_int = sub.add_parser("interactive", help="(optional) interactive mode")
    p_int.set_defaults(func=cmd_interactive)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

