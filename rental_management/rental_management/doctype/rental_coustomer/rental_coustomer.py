import frappe
from frappe import _
from frappe.model.document import Document

class RentalCustomer(Document):
    def validate(self):
        if self.blacklisted and not self.blacklist_reason:
            frappe.throw(_("Please provide a reason for blacklisting this customer."))
        if self.license_expiry_date:
            if frappe.utils.getdate(self.license_expiry_date) < frappe.utils.today():
                frappe.msgprint(_("Warning: This customer's driving license has expired."),
                                alert=True, indicator="red")

    def is_eligible_to_rent(self) -> tuple[bool, str]:
        if self.blacklisted:
            return False, f"Customer is blacklisted: {self.blacklist_reason}"
        if self.license_expiry_date and frappe.utils.getdate(self.license_expiry_date) < frappe.utils.today():
            return False, "Driving license has expired."
        return True, ""
