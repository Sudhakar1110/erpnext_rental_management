# Vehicle Rental Management — ERPNext v15+ App

A complete Vehicle / Fleet Rental Management application for **ERPNext v15+** built on the
**Frappe Framework v15+**.

## Requirements

- Frappe Framework v15+
- ERPNext v15+
- Python 3.10+
- Node.js 18+
- Redis, MariaDB

## Installation

```bash
# 1. Get the app on your bench
cd ~/frappe-bench
bench get-app https://github.com/Sudhakar1110/erpnext_rental_management.git

# 2. Install on your site
bench --site <your-site> install-app vehicle_rental_management
bench --site <your-site> install-app rental_management

# 3. Migrate & restart
bench --site <your-site> migrate
bench restart
```

## DocTypes Created

### Masters
- `Vehicle Category` — Economy, SUV, Luxury, Van ...
- `Vehicle Make` — Toyota, BMW, Ford ...
- `Vehicle Model` — linked to Make
- `Vehicle Location` — branches / pickup points
- `Rental Extra` — GPS, Child Seat, Insurance Top-up ...
- `Rental Pricing Plan` (with child `Rental Pricing Tier`)
- `Driver` / `Driver License`

### Operational
- `Vehicle` — main fleet record
- `Rental Booking` — reservations (submittable, with workflow)
- `Rental Agreement` — signed contract
- `Vehicle Inspection` — pre/post checkout
- `Vehicle Damage` — incident tracking
- `Vehicle Maintenance` — service scheduling & tracking
- `Vehicle Insurance` — policy management
- `Vehicle Document` — registration, permits
- `Fuel Log` — refueling records
- `Telematics Log` — GPS/telemetry data
- `Rental Invoice` — billing wrapper

### Settings
- `Rental Settings` (Single DocType)

## Workflow: Rental Booking

```
Draft → Confirmed → Checked Out → Checked In → Invoiced → Closed
                         ↘ Cancelled
```

Defined in `fixtures/workflow.json`.

## Reports (Script Reports)

- **Fleet Utilization** — % days rented per vehicle
- **Revenue by Vehicle** — earnings breakdown per vehicle
- **Overdue Returns** — late bookings with estimated fees
- **Upcoming Pickups** — next 7/14/30 days schedule
- **Maintenance Schedule** — upcoming service tasks

## Notifications

| Trigger                 | Channel  | Recipient         |
|-------------------------|----------|-------------------|
| Booking Confirmed       | Email    | Customer          |
| Pickup Reminder (24h)   | Email    | Customer          |
| Return Overdue          | Email    | Customer + Manager|
| Insurance Expiry (30d)  | Email    | Fleet Manager     |
| Registration Expiry(30d)| Email    | Fleet Manager     |
| Maintenance Due (3d)    | Email    | Fleet Manager     |

## Customer Portal

- `/rental` — browse available vehicles
- `/book-vehicle?vehicle=<name>` — booking web form
- `/me` — customer dashboard (Frappe built-in)

## Roles & Permissions

- **Fleet Manager** — Full access to all fleet operations
- **Rental Agent** — Daily rental operations, create bookings
- **Mechanic** — Maintenance and inspection access
- **Driver** — Limited view access for assigned drivers
- **Customer** — Portal access (standard Frappe role)

## Integrations

- **Telematics API**: POST `/api/method/vehicle_rental_management.api.telematics.ingest`
- **Payment Gateway**: ERPNext built-in payment integrations (Stripe, Razorpay, PayPal)
- **Web Booking API**: `create_web_booking` whitelisted method for external portals

## Post-Install Checklist

1. Go to **Rental Settings** and configure:
   - Default tax rate, currency, location
   - Rental service item code (create via Item master)
   - Late return fee, excess KM rates
   - Terms & conditions for agreements
2. Create **Vehicle Categories** (e.g., Economy, SUV, Luxury)
3. Create **Vehicle Makes** (e.g., Toyota, BMW, Ford)
4. Create **Vehicle Models** linked to Makes
5. Create **Vehicle Locations** (pickup/return points)
6. Create **Rental Pricing Plans** with tiers for seasonal pricing
7. Add **Vehicles** with photos, rates, and specifications
8. Configure **Notifications** (already seeded as fixtures)
9. Publish the customer portal at `/rental` (already routed in hooks.py)
10. Set up **Telematics** webhook if using GPS tracking

## Development

```bash
# Watch assets during development
bench watch
```

## License

MIT
