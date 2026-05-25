import frappe
from frappe import _

def send_booking_confirmation(doc, method=None):
    try:
        customer_email = frappe.db.get_value("Customer", doc.customer, "email_id")
        if not customer_email:
            return
        subject = _("Rental Booking Confirmed - {0}").format(doc.name)
        message = f"""
        <p>Dear {doc.customer_name},</p>
        <p>Your booking <strong>{doc.name}</strong> is confirmed.</p>
        <ul>
            <li><strong>Vehicle:</strong> {doc.vehicle}</li>
            <li><strong>Start:</strong> {doc.start_date}</li>
            <li><strong>End:</strong> {doc.end_date}</li>
            <li><strong>Total Days:</strong> {doc.total_days}</li>
            <li><strong>Grand Total:</strong> {doc.currency} {doc.grand_total}</li>
        </ul>
        <p>Please bring your driving license and ID proof.</p>
        """
        frappe.sendmail(recipients=[customer_email], subject=subject, message=message)
    except Exception as e:
        frappe.log_error(f"Booking confirmation failed for {doc.name}: {e}", "Rental Notification")

def send_booking_cancellation(doc, method=None):
    try:
        customer_email = frappe.db.get_value("Customer", doc.customer, "email_id")
        if not customer_email:
            return
        subject = _("Rental Booking Cancelled - {0}").format(doc.name)
        message = f"""
        <p>Dear {doc.customer_name},</p>
        <p>Your booking <strong>{doc.name}</strong> has been cancelled.</p>
        <p>Please contact us if this is an error.</p>
        """
        frappe.sendmail(recipients=[customer_email], subject=subject, message=message)
    except Exception as e:
        frappe.log_error(f"Cancellation email failed for {doc.name}: {e}", "Rental Notification")
