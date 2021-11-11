# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'printnode.scenario.mixin']

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        if res is True:
            # Still looks like shit
            self.print_scenarios(action='print_document_on_sales_order')
