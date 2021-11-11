from odoo import api, fields, models


import logging
_logger = logging.getLogger(__name__)



class pos_auto_invoice(models.Model):
    _inherit = "pos.order"

    @api.model
    def create(self, values):
        if 1:
            values['to_invoice'] = True
            created_order = super(pos_auto_invoice, self).create(values)
            created_order.to_invoice = True
            return created_order