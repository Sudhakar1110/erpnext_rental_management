import frappe

@frappe.whitelist(allow_guest=True)
def ingest(vehicle, lat, lng, speed=0, odometer=None, fuel_level=None, ts=None):
    """
    Webhook endpoint for telematics providers.
    POST /api/method/vehicle_rental_management.vehicle_rental_management.api.telematics.ingest
    Add HMAC/token verification before going to production.
    """
    doc = frappe.get_doc({
        "doctype": "Telematics Log",
        "vehicle": vehicle,
        "latitude": lat,
        "longitude": lng,
        "speed": speed,
        "odometer": odometer,
        "fuel_level": fuel_level,
        "timestamp": ts or frappe.utils.now_datetime()
    })
    doc.insert(ignore_permissions=True)

    if odometer:
        frappe.db.set_value("Vehicle", vehicle, "odometer", odometer)

    return {"ok": True, "log": doc.name}


@frappe.whitelist()
def get_vehicle_last_location(vehicle):
    """Get the latest telematics log for a vehicle."""
    log = frappe.get_all(
        "Telematics Log",
        filters={"vehicle": vehicle},
        fields=["latitude", "longitude", "speed", "odometer", "timestamp"],
        order_by="timestamp desc",
        limit=1
    )
    return log[0] if log else None
