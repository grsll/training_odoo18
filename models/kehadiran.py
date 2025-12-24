from odoo import models, fields, api


class KehadiranLine(models.Model):
    _name = "cdn.kehadiran.line"
    _description = "Kehadiran Peserta Line"

    kehadiran_id = fields.Many2one("cdn.kehadiran", string="Kehadiran", ondelete="cascade")
    peserta_id = fields.Many2one("cdn.peserta", string="Peserta")
    no_hp = fields.Char(related="peserta_id.mobile", string="Nomor Hp")
    jenis_kelamin = fields.Selection(related="peserta_id.jenis_kelamin", string="Jenis Kelamin", readonly=True)
    status = fields.Selection([
            ("masuk", "Masuk"),
            ("izin", "Izin"),
            ("sakit", "Sakit"),
            ("alpha", "Alpha"),
        ],
        string="Status Kehadiran",default="masuk",
    )


class Kehadiran(models.Model):
    _name = "cdn.kehadiran"
    _description = "Kehadiran Peserta"
    _rec_name = "tanggal"

    tanggal = fields.Date(string="Tanggal", default=fields.Date.today(), required=True)
    kursus_id = fields.Many2one(comodel_name="cdn.kursus", string="Kursus", required=True)
    session_id = fields.Many2one(comodel_name="cdn.training.session", string="Sesi Kursus", required=True, domain="[('course_id', '=', kursus_id)]")
    kehadiran_line_ids = fields.One2many("cdn.kehadiran.line", "kehadiran_id", string="Daftar Kehadiran")
    state = fields.Selection(string="Status Kehadiran", selection=[("draft", "Draft"), ("confirm", "Confirm"), ("done", "Done")], default="draft",)
    total_hadir = fields.Integer(string="Total Hadir", compute="_compute_total_hadir", store=True)
    nama_instruktur = fields.Many2one(string='Nama Instruktur', related="session_id.instruktur_id")
    
    

    @api.depends("kehadiran_line_ids.status")
    def _compute_total_hadir(self):
        for record in self:
            record.total_hadir = sum(1 for line in record.kehadiran_line_ids if line.status == "masuk")

    @api.onchange("kursus_id")
    def _onchange_kursus_id(self):
        if self.kursus_id:
            peserta_list = self.env["cdn.pendaftaran"].search([("kursus_id", "=", self.kursus_id.id), ("state", "=", "confirm")]).mapped("pendaftar_id")
            lines = [(5,)]
            for peserta in peserta_list:
                lines.append((0,0,{"peserta_id": peserta.id,"status": "masuk",}))
            self.kehadiran_line_ids = lines

    def action_confirm(self):
        for record in self:
            record.state = "confirm" if record.state == "draft" else record.state

    def action_reset(self):
        for record in self:
            record.state = "draft"

    def action_done(self):
        for record in self:
            record.state = "done"
