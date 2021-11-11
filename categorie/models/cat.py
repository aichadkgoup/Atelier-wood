from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import AccessError, UserError

class categ_eco(models.Model):
    _inherit = "product.public.category"
    id_pos = fields.Integer(
        string='Id_cos',
        required=False)
    bol2 = fields.Boolean(default=False,
                          string='Bol2',
                          required=False)
    #ids_eco = fields.One2many('pos.category', 'id_test')
    
    
    
    
        
    def unlink(self): 
        
       for b in self:
           ct = self.env['pos.category'].search([('id_eco', '=', b.id)])
           ct.unlink()
       
       
       
       
     
       return super(categ_eco, self).unlink()
    
    def write(self, values):
        rt = super(categ_eco, self).write(values)
        catg = self.env['pos.category']
        catg_ecom = self.env['pos.category'].search([('id_eco', '=', self.id)])
        if catg_ecom:
            catg_ecom.sudo().write({
                'name': self.name,
#               'bol_eco': True,
    
            })
           
    
            return rt    
    
   
    @api.model    
    def create(self, values):
        y =super(categ_eco, self).create(values)
        if not y.bol2:
            vr = self.env['pos.category'].sudo().create({
            'name': y.name,
            'bol_eco': True,
            'id_eco': y.id,
            })
            y.id_pos = vr.id

        return y

    bol_write = fields.Boolean(default=False,
        string='Bol_write',
        required=False)

  


class Poss(models.Model):
    _inherit = "pos.category"
                                  
                                  
    
    id_eco = fields.Integer(
        string='Id_cos',
        required=False)
    #id_test = fields.Many2one('product.public.category')
                              
    bol_eco = fields.Boolean(default=False,
        string='Bol2',
        required=False)
    
    def onchange_FIELD_NAME(self):

        
      
        varr = self.env['product.public.category'].search([])
        var2 = self.env['pos.category'].search([])
        print("testttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt",varr)
        
        for rec in varr:
        
            
            vr = self.env['pos.category'].sudo().create({
                'name': rec.name,
                'bol_eco': True,
                'id_eco': rec.id,
                })
        for rv in var2:
             vr = self.env['product.public.category'].sudo().create({
            'name': rv.name,
            'id_pos': rv.id,
            'bol2' : True,
            
                
            })
            
        
        
    

    


    
    
    
    def xunlink(self): 
        
       for b in self:
           ct = self.env['product.public.category'].search([('id_pos', '=', b.id)])
           ct.unlink()
       
       
       
       
     
       return super(Poss, self).unlink()
    
   # def unlink(self):
       
          
          
        #for v in x:
            #self.env['product.public.category'].unlink()
            #list = self.env['pos.category'].search([])
            #catg = self.env['product.public.category'].search([])
            #if catg:
               
                  
        #return  super(Poss, self).sudo().unlink()
         
           
        
             

    def xwrite(self, values):
        rt = super(Poss, self).write(values)
        catg = self.env['product.public.category']
        catg_ecom = self.env['product.public.category'].search([('id_pos', '=', self.id)])
        if catg_ecom:
            catg_ecom.sudo().write({
                'name': self.name,
#               'bol_write2': True,
    
            })
            print(self.name)
    
            return rt
    
    

    @api.model 
    def xcreate(self, values):
        rr =  super(Poss, self).create(values)
        if not rr.bol_eco:
            vr = self.env['product.public.category'].sudo().create({
            'name': rr.name,
            'id_pos': rr.id,
            'bol2' : True,
            
                
            })
            rr.id_eco = vr.id
        return  rr
