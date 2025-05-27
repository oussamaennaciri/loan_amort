from typing import List, Dict

def compute_loan_metrics(
    schedule: List[Dict[str, float]]
) -> Dict[str, float]:
    """
    Compute summary metrics from an amortization schedule.

    Args:
        schedule: list of payment records, each with keys
                  'period', 'payment', 'interest', 'principal', 'balance'

    Returns:
        A dict with:
          - num_payments: total number of payments
          - total_payment: sum of all payments
          - total_interest: sum of all interest paid
          - total_principal: sum of all principal repaid
          - average_payment: total_payment / num_payments
    """
    num_payments = len(schedule)
    total_interest = sum(p['interest']   for p in schedule)
    total_principal = sum(p['principal'] for p in schedule)
    total_payment = sum(p['payment']     for p in schedule)
    average_payment = total_payment / num_payments if num_payments else 0.0

    return {
        "num_payments":    num_payments,
        "total_payment":   round(total_payment, 2),
        "total_interest":  round(total_interest, 2),
        "total_principal": round(total_principal, 2),
        "average_payment": round(average_payment, 2),
    }

