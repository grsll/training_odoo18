from odoo import models, fields, api



class Instruktur(models.Model):
    _name = 'cdn.instruktur'
    _description = 'Tabel Instruktur'
    _inherits = {'res.partner': 'partner_id'}
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='ID Partner', ondelete='cascade', required=True)
    keahlian_ids = fields.Many2many(comodel_name='cdn.keahlian', string='Keahlian')
    
    
    

class keahlian(models.Model):
    _name = 'cdn.keahlian'
    _description = 'Tabel Keahlian'
    
    name = fields.Char(string='Nama Keahlian', required=True)
    

    
    
    

    
    
