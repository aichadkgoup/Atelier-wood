from odoo import api, exceptions, fields, models, _
from odoo.exceptions import UserError


class SaleInherits(models.Model):
    _inherit = 'sale.order'