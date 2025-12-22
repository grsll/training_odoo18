from odoo import models, fields, api


class KehadiranLine(models.Model):
    _name = 'cdn.kehadiran.line'
    _description = 'Kehadiran Peserta Line'

    kehadiran_id = fields.Many2one('cdn.kehadiran', string='Kehadiran', ondelete='cascade')
    peserta_id = fields.Many2one('cdn.peserta', string='Peserta',)
    no_hp = fields.Char(related="peserta_id.mobile", string='Nomor Hp')
    jenis_kelamin = fields.Selection(related="peserta_id.jenis_kelamin", string='Jenis Kelamin', readonly=True)
    
    status = fields.Selection([
        ('masuk', 'Masuk'),
        ('izin', 'Izin'),
        ('sakit', 'Sakit'),
        ('alpha', 'Alpha'),
    ], string='Status Kehadiran', default='masuk', )


class Kehadiran(models.Model):
    _name = 'cdn.kehadiran'
    _description = 'Kehadiran Peserta'

    tanggal = fields.Date(string='Tanggal', default=fields.Date.today(), required=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Kursus', required=True)
    session_id = fields.Many2one(comodel_name='cdn.training.session', string='Sesi Kursus', required=True, domain="[('course_id', '=', kursus_id)]")
    peserta_ids = fields.Many2many('cdn.peserta', string='Peserta Terdaftar', compute='_compute_peserta_ids', store=True)
    kehadiran_line_ids = fields.One2many('cdn.kehadiran.line', 'kehadiran_id', string='Daftar Kehadiran')
    state = fields.Selection(string='Status Kehadiran', selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')

    @api.depends('kursus_id')
    def _compute_peserta_ids(self):
        for record in self:
            if record.kursus_id:
                record.peserta_ids = record.kursus_id.pendaftar_ids.mapped('pendaftar_id')
            else:
                record.peserta_ids = self.env['cdn.peserta']

    @api.onchange('kursus_id')
    def _onchange_kursus_id(self):
        if self.kursus_id:
            peserta_list = self.kursus_id.pendaftar_ids.mapped('pendaftar_id')
            lines = [(5,)]  
            for peserta in peserta_list:
                lines.append((0, 0, {
                    'peserta_id': peserta.id,
                    'status': 'masuk',
                }))
            self.kehadiran_line_ids = lines
                
    def action_confirm(self):
        for record in self:
            record.state = 'confirmed' if record.state == 'draft' else record.state
                        
    def action_reset(self):
        for record in self:
            record.state = 'draft'