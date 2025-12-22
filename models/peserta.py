from odoo import models, fields, api


class Peserta(models.Model):
    _name = "cdn.peserta"
    _description = "Tabel Peserta"
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Parther ID",
        required=True,
        ondelete="cascade",
    )
    tanggal_lahir = fields.Date("Tanggal Lahir")
    tempat_lahir = fields.Char(string="Tempat Lahir")
    jenjang_pendidikan = fields.Selection(
        [("sd", "SD"), ("smp", "SMP"), ("sma", "SMA/SMK"), ("s1", "Sarjana S1")],
        string="Jenjang Pendidikan",
    )
    pekerjaan = fields.Char(string="Pekerjaan")
    is_menikah = fields.Boolean(string="Sudah Menikah")
    nama_pasangan = fields.Char(string="Nama Pasangan")
    hp_pasangan = fields.Char(string="HP Pasangan")
    no_peserta = fields.Char(string='No Peserta', readonly=True)
    
    @api.model
    def create(self, vals):
        vals['no_peserta'] = self.env['ir.sequence'].next_by_code('cdn.peserta')
        return super(Peserta, self).create(vals)
        
    
