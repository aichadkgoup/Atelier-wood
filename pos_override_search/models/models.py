# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import pprint
_logger = logging.getLogger(__name__)



class pos_override_search(models.Model):
    _inherit = 'product.product'


    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None ):


        my_domain = ['&', '&', ['sale_ok', '=', True], ['available_in_pos', '=', True], '|', ['company_id', '=', 1], ['company_id', '=', False]]
        ze_domain = ['&', '&','&',['qty_available', '>', 0], ['sale_ok','=',True],['available_in_pos','=',True],'|',['company_id','=',1],['company_id','=',False]]
        # ze_domain_cat = ['&', '&','&',['pos_categ_id', 'in', config.iface_available_categ_ids], ['sale_ok','=',True],['available_in_pos','=',True],'|',['company_id','=',1],['company_id','=',False]]
        if my_domain == domain:
            domain = ze_domain
        else:
             domain.append(['qty_available', '>', 0]);

        return super(pos_override_search, self).search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order)


