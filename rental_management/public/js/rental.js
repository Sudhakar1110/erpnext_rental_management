frappe.ui.form.on("Rental Booking", {
    refresh(frm) {
        const colour_map = {
            Draft: "gray", Confirmed: "blue", Active: "green",
            Completed: "darkgreen", Cancelled: "red",
        };
        frm.page.set_indicator(frm.doc.status, colour_map[frm.doc.status] || "gray");
        if (frm.doc.docstatus === 1) {
            if (frm.doc.status === "Confirmed") {
                frm.add_custom_button(__("Mark as Active"), () => {
                    frappe.confirm(__("Confirm vehicle handover to customer?"),
                        () => frm.call("mark_active").then(() => frm.reload_doc()));
                }, __("Actions"));
            }
            if (frm.doc.status === "Active") {
                frm.add_custom_button(__("Complete Booking"), () => {
                    frappe.confirm(__("Confirm vehicle return and complete this booking?"),
                        () => frm.call("complete_booking").then(() => frm.reload_doc()));
                }, __("Actions"));
            }
            frm.add_custom_button(__("Create Payment"), () => {
                frappe.new_doc("Rental Payment", {
                    booking: frm.doc.name,
                    customer: frm.doc.customer,
                    amount: frm.doc.grand_total,
                    payment_type: "Rental Amount",
                });
            }, __("Actions"));
        }
    },
    start_date(frm) { _recalculate(frm); },
    end_date(frm)   { _recalculate(frm); },
    discount_percent(frm) { _recalculate(frm); },
    vehicle(frm) {
        if (!frm.doc.vehicle) return;
        frappe.db.get_doc("Rental Vehicle", frm.doc.vehicle).then(v => {
            frm.set_value("daily_rate", v.daily_rate);
            frm.set_value("damage_deposit", v.damage_deposit || 0);
            frm.set_value("currency", v.currency || "INR");
            _recalculate(frm);
        });
    },
});

function _recalculate(frm) {
    const { start_date, end_date, daily_rate, discount_percent, damage_deposit } = frm.doc;
    if (!start_date || !end_date || !daily_rate) return;
    const days = frappe.datetime.get_diff(end_date, start_date);
    if (days <= 0) { frappe.msgprint(__("End Date must be after Start Date.")); return; }
    const rental_amount   = days * daily_rate;
    const discount_amount = rental_amount * ((discount_percent || 0) / 100);
    const grand_total     = rental_amount - discount_amount + (damage_deposit || 0);
    frm.set_value("total_days",      days);
    frm.set_value("rental_amount",   rental_amount);
    frm.set_value("discount_amount", discount_amount);
    frm.set_value("grand_total",     grand_total);
}

frappe.ui.form.on("Rental Vehicle", {
    refresh(frm) {
        const colour_map = {
            Available: "green", Rented: "blue", Maintenance: "orange", Retired: "gray"
        };
        frm.page.set_indicator(frm.doc.status, colour_map[frm.doc.status] || "gray");
        if (!frm.is_new()) {
            frm.add_custom_button(__("View Bookings"), () => {
                frappe.set_route("List", "Rental Booking", { vehicle: frm.doc.name });
            });
        }
    },
    daily_rate(frm) {
        const rate = frm.doc.daily_rate;
        if (!rate) return;
        if (!frm.doc.weekly_rate)  frm.set_value("weekly_rate",  +(rate * 6.5).toFixed(2));
        if (!frm.doc.monthly_rate) frm.set_value("monthly_rate", +(rate * 25).toFixed(2));
    },
});

frappe.ui.form.on("Rental Payment", {
    booking(frm) {
        if (!frm.doc.booking) return;
        frappe.db.get_doc("Rental Booking", frm.doc.booking).then(b => {
            if (!frm.doc.customer) frm.set_value("customer", b.customer);
            if (!frm.doc.amount)   frm.set_value("amount", b.grand_total);
        });
    },
});
