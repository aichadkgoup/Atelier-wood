from odoo import api, fields, models, tools, _
from odoo.osv import expression
from odoo.exceptions import AccessError









class labeldescription(models.Model):
    _inherit = "product.template"

    label_description= fields.Char(string='Label description', store=True, index=True)
   


