# ERPNext Rental Management App

A Frappe/ERPNext v15 compatible rental management application for managing vehicles, bookings, customers, payments, and rental analytics.

## Features
- Rental Vehicle – Manage vehicle inventory with availability status, daily rates, and category.
- Rental Booking – Full booking lifecycle: Draft → Confirmed → Active → Completed / Cancelled.
- Rental Payment – Track payments linked to bookings with payment mode and status.
- Rental Customer – Extended customer profile with driving licence and contact details.
- Calculations – Automatic total/damage-deposit calculation, overdue detection.
- API – Whitelisted endpoints for availability check, booking creation, and dashboard stats.

## Installation
bench get-app rental_management <repo-url>
bench --site your-site install-app rental_management
bench migrate

## Requirements
- Frappe Framework >= 15
- ERPNext >= 15
