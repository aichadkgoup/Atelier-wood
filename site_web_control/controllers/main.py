
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class WebsiteSale(http.Controller):
    
    
    @http.route(['/test4', '/test4/page/<int:page>'], type='http', auth="user", website=True)
    def events(self, page=0, search='', **post):
        #tset1 = request.env['res.users'].search([('id', '=', 2)])
        tset1 = request.env['res.partner'].search([('name', '=', request.env.user.partner_id.name)])
        _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888111 %s", tset1)
        nombre_de_contacts = request.env['res.partner'].search_count([('parent_id', '=', tset1.id)])
        _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888222 %s", nombre_de_contacts)
        
       
        _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888 %s", nombre_de_contacts)
        pager = request.website.pager(
            url="/test4",
            total=nombre_de_contacts,
            


            page=page,
            step=3,
           
        )
        _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888333 %s", pager)
        tstt = request.env['res.partner'].sudo().search([('parent_id', '=', tset1.id)],limit=10,offset=pager['offset'])
        _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888333 %s", tstt)
        #self.env['res.users'].browse(2).partner_id.child_ids[offset=pager['offset']:][0:10]
        values = {
    
            'pager': pager,
            'adress' :tstt,
   
        }
        return request.render("website.test4", values)




    @http.route(['/shop/ajouter-adress'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        values, errors = {}, {}
        values = kw
        sess = False
        error = False

        tset1 = request.env['res.partner'].search([('name', '=', request.env.user.partner_id.name)])
        _logger.info("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuukw %s", kw)

        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(
            int(values['country_id']))
        _logger.info("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu3 %s", country)
        
        if 'submitted_edit' in kw:
            
              parent = request.env['res.partner'].search([('id', '=', kw['parter_test'])])
              _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy2222222222299999999lll %s",request.env['res.partner'].search([('id', '=', kw['parter_test'])]))
              values = {'name':parent.name,'tele':parent.phone,'adresse':parent.street,'complement_adress':parent.street2,'code_post':parent.zip,}
              mode = 'edit'

            

        if 'submitted' in kw:
            try:



                _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888 %s", nombre_de_contacts)



                yyy = request.env['res.partner'].sudo().create(
                    {'parent_id': tset1.id, 'name': kw.get('name'), 'phone': kw.get('tele'),
                     'street': kw.get('adresse'), 'street2': kw.get('complement_adress'), 'zip': kw.get('code_post'),
                     'city': kw.get('ville'), 'country_id': int(kw.get('country_id')), 'type': 'contact',
                     'email': 'contact', })
                sess = 'tsest'

                _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy888 %s")
                request.env.cr.commit()
                return request.redirect('/test4',render_values)



            except:
                request.env.cr.rollback()
                _logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy22222222222 %s")
                error = 'Une erreur survenu!veuillez reessayer!'

        
        #_logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy2222222222233388888888888 %s")
        #parent = request.env['res.partner'].search([('id', '=', kw['parter_test'])])
        #_logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy2222222222299999999lll %s",request.env['res.partner'].search([('id', '=', kw['parter_test'])]))
        #values = {'name':parent.name,'tele':parent.phone,'adresse':parent.street,'complement_adress':parent.street2,'code_post':parent.zip,}

        render_values = {

            'checkout': values,
            'sess': sess,
            'error': error,
            'mode':mode,

        }
        

        #_logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy22222222222 %s",render_values['mode'])
        #_logger.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy22222222222999 %s",values)
        render_values['countries'] = request.env["res.country"].search([])
        return request.render("website.ajouter-adress", render_values)
        
        
        
        

                     
                     
                     
                                                   
        
        
     


        






