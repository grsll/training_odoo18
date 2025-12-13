from odoo import models, fields, api


class Kursus(models.Model):
    _name = "cdn.kursus"
    _description = "Tabel Kursus"

    name = fields.Char(string="Nama Kursus")
    description = fields.Text(string="Keterangan")
    user_id = fields.Many2one("res.users", string="Penanggung Jawab")
    session_line = fields.One2many(
        comodel_name="cdn.training.session", inverse_name="course_id", string="Sessions"
    )


class TrainingSession(models.Model):
    _name = "cdn.training.session"
    _description = "TrainingSession"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Session Name", required=True, tracking=True)
    course_id = fields.Many2one(
        comodel_name="cdn.kursus",
        string="Course Name",
        required=True,
        ondelete="cascade",
    )
    start_date = fields.Date(string="Start Date", required=True, tracking=True)
    duration = fields.Float(string="Duration", required=True, tracking=True)
    seats = fields.Integer(string="Seats", tracking=True)

    peserta_ids = fields.Many2many(comodel_name="cdn.peserta", string="Peserta")
    instruktur_id = fields.Many2one(
        comodel_name="cdn.instruktur", string="Instruktur", tracking=True
    )
    no_hp = fields.Char(string="No HP", related="instruktur_id.mobile")
    email = fields.Char(string="Email", related="instruktur_id.email")
    jenis_kelamin = fields.Selection(
        string="Jenis Kelamin", related="instruktur_id.jenis_kelamin"
    )
    jumlah_peserta = fields.Integer(
        string="Jumlah Peserta", compute="_compute_jumlah_peserta"
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Dalam Proses"),
            ("done", "Selesai"),
        ],
        default="draft",
    )

    @api.depends("peserta_ids")
    def _compute_jumlah_peserta(self):
        for record in self:
            record.jumlah_peserta = len(record.peserta_ids)

    def action_confirm(self):
        for record in self:
            record.state = "confirm"

    def action_done(self):
        for record in self:
            record.state = "done"

    def action_reset(self):
        for record in self:
            record.state = "draft"
