# Vehicle Rental Management — ERPNext v15+ App

A complete Vehicle / Fleet Rental Management application for **ERPNext v15+** built on the
**Frappe Framework**. Inspired by Rentsyst (rentsyst.com) and Coastr (coastr.com).

## 🚗 Feature Mapping vs Rentsyst & Coastr

| Feature Area                  | Rentsyst | Coastr | This App (ERPNext v15)            |
|-------------------------------|----------|--------|-----------------------------------|
| Fleet / Vehicle Master        | ✅       | ✅     | `Vehicle` DocType                 |
| Online Booking Engine         | ✅       | ✅     | Web Form `/book-vehicle`          |
| Rental Agreements / Contracts | ✅       | ✅     | `Rental Agreement`                |
| Dynamic Pricing / Seasons     | ✅       | ✅     | `Rental Pricing Plan` + tiers     |
| Extras / Add-ons              | ✅       | ✅     | `Rental Extra`                    |
| Damage / Inspection           | ✅       | ✅     | `Vehicle Inspection`, `Vehicle Damage` |
| Maintenance & Service         | ✅       | ✅     | `Vehicle Maintenance`             |
| Insurance Tracking            | ✅       | ✅     | `Vehicle Insurance`               |
| Driver / KYC Management       | ✅       | ✅     | `Driver`, `Driver License`        |
| Telematics / GPS              | ✅       | ✅     | `Telematics Log` (API ready)      |
| Fuel Logging                  | ✅       | ✅     | `Fuel Log`                        |
| Payments / Invoicing          | ✅       | ✅     | Integrated `Sales Invoice`        |
| Multi-location                | ✅       | ✅     | `Vehicle Location`                |
| Reports & Dashboards          | ✅       | ✅     | 5 Reports + Workspace charts      |
| Customer Portal               | ✅       | ✅     | `/rental` portal                  |
| Notifications (Email/SMS)     | ✅       | ✅     | Frappe `Notification` docs        |

## 📦 Installation

```bash
# 1. Ensure ERPNext v15+ bench is running
bench --version          # Frappe v15+
bench list-apps

# 2. Get the app
cd ~/frappe-bench
bench get-app https://github.com/<your-org>/vehicle_rental_management.git

# 3. Install on site
bench --site <your-site> install-app vehicle_rental_management

# 4. Migrate & restart
bench --site <your-site> migrate
bench restart
```

## 🧱 DocTypes Created

### Masters
- `Vehicle Category` – Economy, SUV, Luxury, Van …
- `Vehicle Make` – Toyota, BMW, Ford …
- `Vehicle Model` – linked to Make
- `Vehicle Location` – branches / pickup points
- `Rental Extra` – GPS, Child Seat, Insurance Top-up …
- `Rental Pricing Plan` (with child `Rental Pricing Tier`)
- `Driver` / `Driver License`

### Operational
- `Vehicle` – main fleet record
- `Rental Booking` – reservations
- `Rental Agreement` – signed contract
- `Vehicle Inspection` – pre/post checkout
- `Vehicle Damage`
- `Vehicle Maintenance`
- `Vehicle Insurance`
- `Vehicle Document` (registration, permits)
- `Fuel Log`
- `Telematics Log`
- `Rental Invoice` (wraps Sales Invoice)

### Settings
- `Rental Settings` (Single DocType)

## 🔄 Workflow: Rental Booking

```
Draft → Confirmed → Checked Out → Checked In → Invoiced → Closed
                         ↘ Cancelled
```

Defined in `fixtures/workflow.json`.

## 📊 Reports (Script Reports)
- **Fleet Utilization** – % days rented per vehicle
- **Revenue by Vehicle**
- **Overdue Returns**
- **Upcoming Pickups**
- **Maintenance Schedule**

## 🔔 Notifications

| Trigger                    | Channel      | Recipient               |
|----------------------------|--------------|-------------------------|
| Booking Confirmed          | Email        | Customer                |
| Pickup Reminder (24h)      | Email + SMS  | Customer                |
| Return Overdue             | Email        | Customer + Manager      |
| Insurance Expiry (30 days) | Email        | Fleet Manager           |
| License Expiry (30 days)   | Email        | Driver                  |
| Maintenance Due            | Email        | Fleet Manager           |

## 🌐 Customer Portal
- `/rental` – browse vehicles
- `/book-vehicle` – booking web form
- `/me` – customer dashboard (Frappe built-in)

## 🔐 Roles
- Fleet Manager
- Rental Agent
- Mechanic
- Driver
- Customer (standard portal role)

## 🔌 Integrations Ready
- Payment Gateway (ERPNext Payment Gateway)
- Telematics webhook: `/api/method/vehicle_rental_management.api.telematics.ingest`
- Stripe / Razorpay / PayPal via ERPNext

## ✅ Post-Install Checklist
1. Set up **Rental Settings** (default location, tax, terms).
2. Create **Vehicle Categories** and **Pricing Plans**.
3. Add **Vehicles** with photos.
4. Configure **Notifications** in Setup.
5. Publish web form `/book-vehicle`.

## 🧭 Push to Git

```bash
git init
git add .
git commit -m "feat: initial ERPNext v15 Vehicle Rental Management app"
git branch -M main
git remote add origin https://github.com/<your-org>/vehicle_rental_management.git
git push -u origin main
```
