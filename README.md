# Vehicle Rental Management (ERPNext v15+)

Complete fleet & rental management built on **Frappe/ERPNext v15+**.
Feature-parity with leading rental management platforms.

## Quick Install

```bash
bench get-app https://github.com/Sudhakar1110/erpnext_rental_management.git
bench --site <site> install-app vehicle_rental_management
bench --site <site> install-app rental_management
bench --site <site> migrate
bench restart
```

## Key Features

- **Fleet Management** — Vehicle, Category, Make, Model, Location masters
- **Rental Operations** — Booking, Agreement, Check-in/Check-out workflow
- **Customer Portal** — Browse vehicles and book online at `/rental`
- **Pricing & Extras** — Dynamic pricing plans, seasonal tiers, add-ons
- **Inspections & Damage** — Pre/post rental inspection checklists
- **Maintenance Tracking** — Service schedules, cost tracking, odometer sync
- **Insurance & Documents** — Policy tracking, expiry alerts
- **Telematics Integration** — GPS/webhook ingestion API ready
- **Driver/KYC Management** — Driver profiles, license tracking
- **Reports & Dashboards** — Fleet utilization, revenue analytics, overdue tracking
- **Notifications** — Booking confirmation, pickup reminders, overdue alerts

## License

MIT

For full installation guide and feature details, see [SETUP.md](./SETUP.md).
