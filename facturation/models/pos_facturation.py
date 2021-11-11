from odoo import api, fields, models




class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def create(self, values):
        if 1:
            values['to_invoice'] = True
            created_order = super(PosOrder, self).create(values)
            created_order.to_invoice = True
        

