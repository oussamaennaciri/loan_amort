import click
import pandas as pd
import matplotlib.pyplot as plt
from loan_amort.amort import amortize_loan

@click.command()
@click.option('--principal',      type=float,                   required=True, help="Loan principal amount")
@click.option('--annual-rate',    type=float,                   required=True, help="Annual interest rate (e.g. 0.06)")
@click.option('--term-months',    type=int,                     required=True, help="Total number of months")
@click.option('--start-date',     type=str,                     required=True, help="First payment date (YYYY-MM-DD)")
@click.option('--loan-type',      type=click.Choice(['amortizing','bullet','interest-only']), default='amortizing', help="Loan type")
@click.option('--output',         type=click.Path(),            default=None, help="CSV output file")
@click.option('--plot/--no-plot', default=False,                help="Generate charts")
def main(principal, annual_rate, term_months, start_date, loan_type, output, plot):
    \"\"\"Generate a loan amortization schedule.\"\"\"
    df = amortize_loan(principal, annual_rate, term_months, start_date, loan_type)

    # Output schedule
    if output:
        df.to_csv(output, index=False)
        click.echo(f"Schedule saved to {output}")
    else:
        click.echo(df.to_string(index=False))

    # Optional plots
    if plot:
        # Balance vs Time
        plt.figure()
        plt.plot(df['date'], df['ending_balance'])
        plt.title('Balance vs. Time')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.savefig('balance_vs_time.png')
        click.echo("Saved balance_vs_time.png")

        # Interest vs Principal
        plt.figure()
        plt.plot(df['date'], df['interest'], label='Interest')
        plt.plot(df['date'], df['principal'], label='Principal')
        plt.title('Interest vs. Principal')
        plt.xlabel('Date')
        plt.legend()
        plt.savefig('interest_vs_principal.png')
        click.echo("Saved interest_vs_principal.png")

if __name__ == '__main__':
    main()
