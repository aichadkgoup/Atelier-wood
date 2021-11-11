# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    pricing_grid = fields.Html('Price list')
    import_name = fields.Char('Import Name excel')
    zip_start_by = fields.Char('Zip start by', help="Check if the ZIP code start with this char, You can use multi item separed by space or coma")


    def _match_address(self, partner):
        "add zip_start_by matching"
        res = super()._match_address(partner)

        if res and self.zip_start_by:
            zip_text = (self.zip_start_by or '').upper()
            zip_text = zip_text.replace(',', ' ').replace('   ', ' ').replace('  ', ' ').strip()
            zip_list =  zip_text.split(' ')
            check_zip = False
            zip_partner = (partner.zip or '').strip()

            for zip_start in zip_list:
                if len(zip_start) <= len(zip_partner):
                    if zip_partner[:len(zip_start)] == zip_start:
                        check_zip = True
                if check_zip:
                    break

            if zip_list and not check_zip:
                res = False

        return res

