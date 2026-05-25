app_name = "vehicle_rental_management"
app_title = "Vehicle Rental Management"
app_publisher = "Your Company"
app_description = "Vehicle Rental & Fleet Management for ERPNext v15+"
app_email = "dev@example.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

app_include_css = "/assets/vehicle_rental_management/css/vrm.css"
app_include_js  = "/assets/vehicle_rental_management/js/vrm.js"
web_include_css = "/assets/vehicle_rental_management/css/vrm.css"
web_include_js  = "/assets/vehicle_rental_management/js/vrm.js"

fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Fleet Manager", "Rental Agent", "Mechanic", "Driver"
    ]]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Vehicle Rental Management"]]},
    {"dt": "Workflow", "filters": [["name", "in", ["Rental Booking Workflow"]]]},
    {"dt": "Notification", "filters": [["module", "=", "Vehicle Rental Management"]]},
]

doc_events = {
    "Rental Booking": {
        "validate": "vehicle_rental_management.doctype.rental_booking.rental_booking.validate_booking",
        "on_submit": "vehicle_rental_management.doctype.rental_booking.rental_booking.on_submit_booking",
        "on_cancel": "vehicle_rental_management.doctype.rental_booking.rental_booking.on_cancel_booking",
    },
    "Rental Agreement": {
        "on_submit": "vehicle_rental_management.doctype.rental_agreement.rental_agreement.create_sales_invoice"
    },
}

scheduler_events = {
    "daily": [
        "vehicle_rental_management.tasks.send_pickup_reminders",
        "vehicle_rental_management.tasks.check_overdue_returns",
        "vehicle_rental_management.tasks.check_document_expiry",
        "vehicle_rental_management.tasks.check_maintenance_due",
    ],
    "hourly": [
        "vehicle_rental_management.tasks.sync_telematics",
    ],
}

website_route_rules = [
    {"from_route": "/rental", "to_route": "rental"},
]

after_install = "vehicle_rental_management.install.after_install"
