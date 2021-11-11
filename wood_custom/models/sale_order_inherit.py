from odoo import api, exceptions, fields, models, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    date_production = fields.Date(string='date production')

    display_name = fields.Char(string='display name',compute='_compute_desplay')


    @api.depends('name', 'partner_id.name')
    def _compute_desplay(self):
        for var in self:
            var.display_name = str(var.name) + " " + var.partner_id.name

