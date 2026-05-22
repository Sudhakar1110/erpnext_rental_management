import frappe
from frappe import _
from rental_management.utils.calculations import (
    calculate_rental_days, calculate_rental_amount,
    calculate_discount, calculate_grand_total,
)

@frappe.whitelist()
def get_bookings(status=None, customer=None, vehicle=None, from_date=None, to_date=None):
    filters = {"docstatus": ["!=", 2]}
    if status:   filters["status"] = status
    if customer: filters["customer"] = customer
    if vehicle:  filters["vehicle"] = vehicle
    if from_date: filters["start_date"] = [">=", from_date]
    if to_date:   filters["end_date"] = ["<=", to_date]
    bookings = frappe.get_all("Rental Booking", filters=filters,
        fields=["name","customer","customer_name","vehicle","start_date","end_date","total_days","grand_total","status","currency"],
        order_by="start_date desc", limit=100)
    return {"status": "success", "data": bookings, "count": len(bookings)}

@frappe.whitelist()
def check_vehicle_availability(vehicle, start_date, end_date):
    v = frappe.get_doc("Rental Vehicle", vehicle)
    if v.status in ("Maintenance", "Retired"):
        return {"status": "success", "available": False, "reason": f"Vehicle is {v.status}.", "conflicts": []}
    conflicts = frappe.db.sql("""
        SELECT name, start_date, end_date, customer_name FROM `tabRental Booking`
        WHERE vehicle=%(vehicle)s AND docstatus=1 AND status IN ('Confirmed','Active')
        AND NOT (end_date <= %(start_date)s OR start_date >= %(end_date)s)
    """, {"vehicle": vehicle, "start_date": start_date, "end_date": end_date}, as_dict=True)
    return {"status": "success", "available": len(conflicts) == 0,
            "reason": "" if not conflicts else "Conflicting bookings exist.", "conflicts": conflicts}

@frappe.whitelist()
def calculate_booking_cost(vehicle, start_date, end_date, discount_percent=0):
    v = frappe.get_doc("Rental Vehicle", vehicle)
    days = calculate_rental_days(start_date, end_date)
    rental_amount = calculate_rental_amount(days, v.daily_rate)
    discount_amount = calculate_discount(rental_amount, float(discount_percent))
    grand_total = calculate_grand_total(rental_amount, discount_amount, v.damage_deposit or 0)
    return {"status": "success", "vehicle": vehicle, "vehicle_name": v.vehicle_name,
            "days": days, "daily_rate": v.daily_rate, "rental_amount": rental_amount,
            "damage_deposit": v.damage_deposit or 0, "discount_amount": discount_amount,
            "grand_total": grand_total, "currency": v.currency or "INR"}

@frappe.whitelist()
def create_booking(customer, vehicle, start_date, end_date, discount_percent=0,
                   driver_name=None, driving_license_no=None, pickup_location=None,
                   return_location=None, remarks=None):
    rc = frappe.db.get_value("Rental Customer", {"customer": customer}, ["blacklisted","blacklist_reason"], as_dict=True)
    if rc and rc.blacklisted:
        frappe.throw(_("Customer is blacklisted: {0}").format(rc.blacklist_reason))
    doc = frappe.new_doc("Rental Booking")
    doc.update({"customer": customer, "vehicle": vehicle, "start_date": start_date,
                 "end_date": end_date, "discount_percent": float(discount_percent),
                 "driver_name": driver_name, "driving_license_no": driving_license_no,
                 "pickup_location": pickup_location, "return_location": return_location, "remarks": remarks})
    doc.insert()
    return {"status": "success", "booking": doc.name}

@frappe.whitelist()
def get_dashboard_stats():
    active = frappe.db.count("Rental Booking", {"status": "Active", "docstatus": 1})
    confirmed = frappe.db.count("Rental Booking", {"status": "Confirmed", "docstatus": 1})
    available = frappe.db.count("Rental Vehicle", {"status": "Available"})
    total = frappe.db.count("Rental Vehicle", {"status": ["!=", "Retired"]})
    revenue = frappe.db.sql("""SELECT COALESCE(SUM(grand_total),0) FROM `tabRental Booking`
        WHERE status='Completed' AND docstatus=1
        AND MONTH(end_date)=MONTH(CURDATE()) AND YEAR(end_date)=YEAR(CURDATE())""")
    overdue = frappe.db.count("Rental Booking", {"status": "Active", "end_date": ["<", frappe.utils.today()], "docstatus": 1})
    return {"status": "success", "active_bookings": active, "confirmed_bookings": confirmed,
            "available_vehicles": available, "total_vehicles": total,
            "monthly_revenue": float(revenue[0][0] if revenue else 0), "overdue_bookings": overdue}
