import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class RentalPricingPlan(Document):

    def get_rate_for_date(self, date):
        """Return daily rate applicable for a given date (checks seasonal tiers first)."""
        for tier in self.tiers:
            if tier.from_date and tier.to_date:
                if getdate(tier.from_date) <= getdate(date) <= getdate(tier.to_date):
                    return tier.daily_rate
        return self.base_daily_rate
