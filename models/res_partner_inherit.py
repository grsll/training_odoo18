from odoo import models, fields, api



class ResPartner(models.Model):
    _inherit = "res.partner"

    propinsi_id = fields.Many2one(comodel_name='cdn.propinsi', string='Propinsi')
    kota_id = fields.Many2one(comodel_name='cdn.kota', string='Kota')
    kecamatan_id = fields.Many2one(comodel_name='cdn.kecamatan', string='Kecamatan')
    desa_id = fields.Many2one(comodel_name='cdn.desa', string='Desa/Kelurahan')
    jenis_kelamin = fields.Selection([
        ('laki-laki', 'Laki-Laki'),
        ('perempuan', 'Perempuan')
    ], string='Jenis Kelamin')
    
    
    
    