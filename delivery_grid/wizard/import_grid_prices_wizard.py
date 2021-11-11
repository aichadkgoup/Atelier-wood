# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import base64
import xlrd
from odoo.exceptions import UserError

def to_float(value):
    "return float value"
    if not value:
        return 0.0
    elif isinstance(value, float):
        return value
    elif isinstance(value, int):
        return float(value)
    else:
        for item in ['€', 'EUR', 'Kg', 'kg', '   ', '  ']:
            value = value.replace(item, ' ')
        value = value.replace(',', '.')
        try:
            value = float(value)
        except:
            value = 0.0
    return value

class ImportGridPricesWizard(models.Model):
    _name = 'import.grid.prices.wizard'

    import_file = fields.Binary('Import File', attachment=False)
    note = fields.Text('Log')

    def import_grid_service(self):
        delivery_obj = self.env['delivery.carrier']
        product_obj = self.env['product.product']
        delivery_price_obj = self.env['delivery.price.rule']
        note = ''
        if self.import_file:
            text_to_import = base64.b64decode(self.import_file)
            try:
                book = xlrd.open_workbook(file_contents=text_to_import)
            except:
                raise UserError(_('Incorrect format. Please try to save the file in Excel 97-2003 format first.'))

            first_sheet = book.sheet_by_index(0)

            if first_sheet.nrows == 0:
                note += _('File is empty\n')
            else:
                note += 'Import Transports Services' + '\n'
                note += '==========================\n'

                product_id = product_obj.search([('name', '=', 'Frais de port')])
                i = 1
                while i < first_sheet.ncols:
                    htmltable = '<table class="table table-condensed table-striped" style="border: 2px solid #ddd;margin-top: 20px;width: 400px;"><thead>' + \
                                '<tr><th style="border: 2px solid #ddd;width: 100px"><strong>Poids</strong></th>' + \
                                '<th style="border: 2px solid #ddd;width: 100px"><strong>Price</strong></th></tr>'

                    import_name = "%s Zone %s" % (first_sheet.cell(0, 0).value, first_sheet.cell(1, i).value)
                    carrier_id = delivery_obj.search([('delivery_type', '=', 'base_on_rule'), ('import_name', '=', import_name)])

                    if not carrier_id:
                        carrier_id = delivery_obj.create({'name': import_name,
                                                          'delivery_type': 'base_on_rule',
                                                          'product_id': product_id.id,
                                                          'import_name': import_name,
                                                          })

                    for row_id in range(2, first_sheet.nrows):
                        htmltable += '<tr><td style="border: 2px solid #ddd;" id="mtp_lig_col_' + str(row_id) +'0">' + str(first_sheet.cell(row_id, 0).value) + '</td>' +\
                                     '<td style="border: 2px solid #ddd;" id="mtp_lig_col_' + str(row_id) +'1">' + str(first_sheet.cell(row_id, i).value) + '</td></tr>'

                        #list_base_price = float(str(first_sheet.cell(row_id, i).value).replace(',', '.').split('€')[0]) if str(first_sheet.cell(row_id, i).value).replace(',', '.') .split('€') else None
                        list_base_price = to_float(first_sheet.cell(row_id, i).value)

                        if list_base_price:
                            #max_value = float(str(first_sheet.cell(row_id, 0).value).split(' -')[1]) if len(str(first_sheet.cell(row_id, 0).value).split('-')) > 1 and str(first_sheet.cell(row_id, 0).value).split('-') else None
                            max_value = to_float(first_sheet.cell(row_id, 0).value.split('-')[-1])
                            delivery_price_id = delivery_price_obj.search(
                                [('max_value', '=', max_value), ('carrier_id', '=', carrier_id.id)])
                            if max_value:
                                if not delivery_price_id:
                                    delivery_price_obj.create({
                                                                'max_value': max_value,
                                                                'sequence': int(max_value),
                                                                'list_base_price': list_base_price,
                                                                'carrier_id': carrier_id.id,
                                                               })
                                else:
                                    delivery_price_id.update({
                                        'list_base_price': list_base_price, 'sequence': int(max_value),
                                    })

                    carrier_id.update({'pricing_grid': htmltable})

                    i += 1
                note += _("Import successfully")
        else:
            note += _("No data file to import")

        self.note = note
        resource_id = self.env.ref('delivery_grid.import_result_view')
        return {
            'name': _('Import File result'),
            'res_id': self.ids[0],
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.grid.prices.wizard',
            'view_id': False,
            'target': 'new',
            'views': [(resource_id.id, 'form')],
            'type': 'ir.actions.act_window',
        }
