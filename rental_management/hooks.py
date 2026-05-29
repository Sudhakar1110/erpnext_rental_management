app_name = "rental_management"
app_title = "Rental Management"
app_publisher = "Your Company"
app_description = "Vehicle rental management for ERPNext v15"
app_email = "admin@yourcompany.com"
app_license = "MIT"
app_version = "1.0.0"
required_apps = ["frappe>=15.0.0"]

app_include_js = ["/assets/rental_management/js/rental.js"]
app_include_css = ["/assets/rental_management/css/rental.css"]

scheduler_events = {
    "daily": [
        "rental_management.utils.scheduler.mark_overdue_bookings",
    ],
}

doc_events = {
    "Rental Booking": {
        "on_submit": "rental_management.utils.notifications.send_booking_confirmation",
        "on_cancel": "rental_management.utils.notifications.send_booking_cancellation",
    }
}
