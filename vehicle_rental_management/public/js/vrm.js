// Vehicle Rental Management - Client-side Scripts

frappe.provide("vrm");

vrm.utils = {
    format_currency: function(value, currency) {
        return frappe.format(value, { fieldtype: "Currency", currency: currency });
    }
};

// Rental Booking form client script
frappe.ui.form.on("Rental Booking", {
    vehicle: function(frm) {
        if (frm.doc.vehicle) {
            frappe.db.get_value("Vehicle", frm.doc.vehicle, ["daily_rate", "pricing_plan", "deposit_amount"], function(r) {
                if (r) {
                    frm.set_value("daily_rate", r.daily_rate);
                    frm.set_value("pricing_plan", r.pricing_plan);
                    frm.set_value("deposit_amount", r.deposit_amount);
                    frm.trigger("compute_totals");
                }
            });
        }
    },

    pickup_date: function(frm) { frm.trigger("compute_totals"); },
    return_date: function(frm) { frm.trigger("compute_totals"); },
    daily_rate: function(frm) { frm.trigger("compute_totals"); },
    discount_amount: function(frm) { frm.trigger("compute_totals"); },

    compute_totals: function(frm) {
        if (!frm.doc.pickup_date || !frm.doc.return_date || !frm.doc.daily_rate) return;

        var pickup = frappe.datetime.str_to_obj(frm.doc.pickup_date);
        var ret = frappe.datetime.str_to_obj(frm.doc.return_date);
        var days = Math.max(1, Math.ceil((ret - pickup) / (1000 * 60 * 60 * 24)));

        frm.set_value("rental_days", days);
        var base = days * flt(frm.doc.daily_rate);
        frm.set_value("base_amount", base);

        var extras = 0;
        (frm.doc.extras || []).forEach(function(e) { extras += flt(e.amount); });
        frm.set_value("extras_total", extras);

        var subtotal = base + extras - flt(frm.doc.discount_amount);
        frm.call("get_tax_rate").then(function(r) {
            var tax = subtotal * flt(r.message || 0) / 100;
            frm.set_value("tax_amount", tax);
            frm.set_value("grand_total", subtotal + tax);
        });
    },

    onload: function(frm) {
        frm.set_query("vehicle", function() {
            return {
                filters: { "status": "Available" }
            };
        });
    }
});

// Vehicle form
frappe.ui.form.on("Vehicle", {
    refresh: function(frm) {
        if (frm.doc.name) {
            frm.add_custom_button(__("View Bookings"), function() {
                frappe.set_route("List", "Rental Booking", {"vehicle": frm.doc.name});
            }, __("View"));
            frm.add_custom_button(__("View Maintenance"), function() {
                frappe.set_route("List", "Vehicle Maintenance", {"vehicle": frm.doc.name});
            }, __("View"));
            frm.add_custom_button(__("New Inspection"), function() {
                frappe.new_doc("Vehicle Inspection", {"vehicle": frm.doc.name});
            }, __("Create"));
        }
    }
});
