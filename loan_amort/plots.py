# loan_amort/plots.py

from typing import List, Dict, Any
import itertools
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import numpy as np

# Styling constants
MINT_BBOX = dict(facecolor="#AAF0D1", edgecolor="black")
DARK_BLUE = "#1f77b4"
DARK_RED = "#d62728"
YEAR_INTERVAL = 5  # show tick every 5 years


def _configure_year_axis(ax, dates: List[datetime.date]) -> None:
    """
    Configure an axis to show year-only ticks at fixed intervals.
    """
    locator = mdates.YearLocator(base=YEAR_INTERVAL)
    formatter = mdates.DateFormatter('%Y')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')


def plot_balance_line(schedule: List[Dict[str, Any]]) -> plt.Figure:
    """
    Line chart of remaining loan balance over time with currency formatting.
    """
    dates = [datetime.date.fromisoformat(p['date']) if isinstance(p.get('date'), str) else p.get('date') for p in schedule]
    balances = [p['balance'] for p in schedule]

    fig, ax = plt.subplots()
    ax.plot(dates, balances, color=DARK_BLUE, label='Balance')
    ax.set_xlabel('Year')
    ax.set_ylabel('Remaining Balance (USD)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Loan Balance Over Time')
    ax.grid(True)
    ax.legend()
    _configure_year_axis(ax, dates)

    marker, = ax.plot([], [], 'o', color='black', markersize=8)
    annot = ax.annotate('', xy=(0,0), xytext=(15,15), textcoords='offset points', bbox=MINT_BBOX)
    annot.set_visible(False)

    def on_move(event):
        if event.inaxes != ax or event.xdata is None:
            return
        xdate = mdates.num2date(event.xdata).date()
        idx = min(range(len(dates)), key=lambda i: abs((dates[i] - xdate).days))
        xpt = dates[idx]
        ypt = balances[idx]
        marker.set_data([xpt], [ypt]); marker.set_visible(True)
        annot.xy = (xpt, ypt)
        # Full date shown
        annot.set_text(f"Date: {xpt.isoformat()}\nBalance: ${ypt:,.2f}")
        annot.set_visible(True)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)
    return fig


def plot_interest_principal_line(schedule: List[Dict[str, Any]]) -> plt.Figure:
    """
    Line chart of interest vs principal with currency formatting.
    """
    dates = [datetime.date.fromisoformat(p['date']) if isinstance(p.get('date'), str) else p.get('date') for p in schedule]
    interests = [p['interest'] for p in schedule]
    principals = [p['principal'] for p in schedule]

    fig, ax = plt.subplots()
    ax.plot(dates, interests, color=DARK_RED, label='Interest')
    ax.plot(dates, principals, color=DARK_BLUE, label='Principal')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount (USD)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Interest vs Principal Over Time')
    ax.grid(True)
    ax.legend()
    _configure_year_axis(ax, dates)

    marker_i, = ax.plot([], [], 'o', color=DARK_RED, markersize=6)
    marker_p, = ax.plot([], [], 'o', color=DARK_BLUE, markersize=6)
    annot = ax.annotate('', xy=(0,0), xytext=(15,15), textcoords='offset points', bbox=MINT_BBOX)
    annot.set_visible(False)

    def on_move(event):
        if event.inaxes != ax or event.xdata is None:
            return
        xdate = mdates.num2date(event.xdata).date()
        idx = min(range(len(dates)), key=lambda i: abs((dates[i] - xdate).days))
        xpt = dates[idx]
        yi = interests[idx]
        yp = principals[idx]
        marker_i.set_data([xpt], [yi]); marker_i.set_visible(True)
        marker_p.set_data([xpt], [yp]); marker_p.set_visible(True)
        ytop = max(yi, yp)
        annot.xy = (xpt, ytop)
        # Full date shown
        annot.set_text(f"Date: {xpt.isoformat()}\nInterest: ${yi:,.2f}\nPrincipal: ${yp:,.2f}")
        annot.set_visible(True)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)
    return fig


def plot_cumulative_line(schedule: List[Dict[str, Any]]) -> plt.Figure:
    """
    Line chart of cumulative interest vs principal with currency formatting, matching interest/principal style.
    """
    dates = [datetime.date.fromisoformat(p['date']) if isinstance(p.get('date'), str) else p.get('date') for p in schedule]
    cum_int = list(itertools.accumulate(p['interest'] for p in schedule))
    cum_pr = list(itertools.accumulate(p['principal'] for p in schedule))

    fig, ax = plt.subplots()
    ax.plot(dates, cum_int, color=DARK_RED, label='Cumulative Interest')
    ax.plot(dates, cum_pr, color=DARK_BLUE, label='Cumulative Principal')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Amount (USD)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Cumulative Interest vs Principal')
    ax.grid(True)
    ax.legend()
    _configure_year_axis(ax, dates)

    marker_i, = ax.plot([], [], 'o', color=DARK_RED, markersize=6)
    marker_p, = ax.plot([], [], 'o', color=DARK_BLUE, markersize=6)
    annot = ax.annotate('', xy=(0,0), xytext=(15,15), textcoords='offset points', bbox=MINT_BBOX)
    annot.set_visible(False)

    def on_move(event):
        if event.inaxes != ax or event.xdata is None:
            return
        xdate = mdates.num2date(event.xdata).date()
        idx = min(range(len(dates)), key=lambda i: abs((dates[i] - xdate).days))
        xpt = dates[idx]
        yi = cum_int[idx]
        yp = cum_pr[idx]
        marker_i.set_data([xpt], [yi]); marker_i.set_visible(True)
        marker_p.set_data([xpt], [yp]); marker_p.set_visible(True)
        ytop = max(yi, yp)
        annot.xy = (xpt, ytop)
        # Full date shown
        annot.set_text(f"Date: {xpt.isoformat()}\nCumulative Interest: ${yi:,.2f}\nCumulative Principal: ${yp:,.2f}")
        annot.set_visible(True)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_move)
    return fig

# Remaining bar plots unchanged

def plot_balance_bar(schedule: List[Dict[str, Any]]) -> plt.Figure:
    dates = [datetime.date.fromisoformat(p['date']) if isinstance(p.get('date'), str) else p.get('date') for p in schedule]
    balances = [p['balance'] for p in schedule]
    fig, ax = plt.subplots()
    ax.bar(dates, balances, color=DARK_BLUE)
    ax.set_xlabel('Year')
    ax.set_ylabel('Balance (USD)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Balance Bar Chart')
    ax.grid(True, axis='y')
    _configure_year_axis(ax, dates)
    return fig


def plot_interest_principal_stacked(schedule: List[Dict[str, Any]]) -> plt.Figure:
    dates = [datetime.date.fromisoformat(p['date']) if isinstance(p.get('date'), str) else p.get('date') for p in schedule]
    interests = [p['interest'] for p in schedule]
    principals = [p['principal'] for p in schedule]
    fig, ax = plt.subplots()
    dates_num = mdates.date2num(dates)
    width = float(np.min(np.diff(dates_num))) * 0.8 if len(dates_num) > 1 else 0.8
    ax.bar(dates, interests, label='Interest', color=DARK_RED, width=width)
    ax.bar(dates, principals, bottom=interests, label='Principal', color=DARK_BLUE, width=width)
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount (USD)')
    ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.2f}'))
    ax.set_title('Interest vs Principal (Stacked)')
    ax.legend()
    ax.grid(True, axis='y')
    _configure_year_axis(ax, dates)
    fig.tight_layout()
    return fig

