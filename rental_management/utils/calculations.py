from datetime import date

def calculate_rental_days(start_date, end_date) -> int:
    if hasattr(start_date, "strftime"):
        delta = end_date - start_date
    else:
        from frappe.utils import getdate
        delta = getdate(end_date) - getdate(start_date)
    days = delta.days
    if days <= 0:
        raise ValueError("end_date must be after start_date")
    return days

def calculate_rental_amount(days: int, daily_rate: float) -> float:
    return round(float(days) * float(daily_rate), 2)

def calculate_discount(rental_amount: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("discount_percent must be between 0 and 100")
    return round(float(rental_amount) * float(discount_percent) / 100, 2)

def calculate_grand_total(rental_amount: float, discount_amount: float, damage_deposit: float = 0.0) -> float:
    return round(float(rental_amount) - float(discount_amount) + float(damage_deposit), 2)

def calculate_overdue_charges(end_date, return_date, daily_rate: float, penalty_multiplier: float = 1.5) -> float:
    from frappe.utils import getdate
    overdue_days = (getdate(return_date) - getdate(end_date)).days
    if overdue_days <= 0:
        return 0.0
    return round(overdue_days * float(daily_rate) * float(penalty_multiplier), 2)

def effective_rate_for_days(days: int, daily_rate: float, weekly_rate: float = 0.0, monthly_rate: float = 0.0) -> float:
    if monthly_rate and days >= 28:
        return round(float(monthly_rate) * (days / 30), 2)
    if weekly_rate and days >= 7:
        return round(float(weekly_rate) * (days // 7) + float(daily_rate) * (days % 7), 2)
    return calculate_rental_amount(days, daily_rate)
