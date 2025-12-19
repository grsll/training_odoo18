from odoo import models, fields, api


class KehadiranLine(models.Model):
    _name = 'cdn.kehadiran.line'
    _description = 'Kehadiran Line'

    kehadiran_id = fields.Many2one('cdn.kehadiran', string='Kehadiran')
    peserta_id = fields.Many2one('cdn.peserta', string='Peserta')
    status = fields.Selection([
        ('hadir', 'Hadir'),
        ('ijin', 'Ijin'),
        ('sakit', 'Sakit'),
        ('alpa', 'Alpa'),
    ], string='Status', default='hadir')


class Kehadiran(models.Model):
    _name = 'cdn.kehadiran'
    _description = 'Kehadiran Peserta'

    tanggal = fields.Date(string='Tanggal', default=fields.Date.today(), required=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Kursus', required=True)
    session_id = fields.Many2one(comodel_name='cdn.training.session', string='Sesi Kursus', required=True, domain="[('course_id', '=', kursus_id)]")
    line_ids = fields.One2many('cdn.kehadiran.line', 'kehadiran_id', string='Lines')
    peserta_ids = fields.Many2many('cdn.peserta', string='Peserta Terdaftar', compute='_compute_peserta_ids', store=True)

    @api.depends('line_ids')
    def _compute_peserta_ids(self):
        for record in self:
            record.peserta_ids = record.line_ids.mapped('peserta_id')

    @api.onchange('kursus_id')
    def _onchange_kursus_id(self):
        if self.kursus_id and not self.line_ids:
            peserta = self.kursus_id.pendaftar_ids.mapped('pendaftar_id')
            self.line_ids = [(0, 0, {'peserta_id': p.id}) for p in peserta]