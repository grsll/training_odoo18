from odoo import models, fields, api
from odoo.exceptions import UserError


class Kursus(models.Model):
    _name = "cdn.kursus"
    _description = "Tabel Kursus"

    name = fields.Char(string="Nama Kursus")
    description = fields.Text(string="Keterangan")
    user_id = fields.Many2one("res.users", string="Penanggung Jawab")
    session_line = fields.One2many(comodel_name="cdn.training.session", inverse_name="course_id", string="Sessions")
    produk_ids = fields.Many2many(comodel_name='product.product', string='Produk Konsumsi')
    total_harga = fields.Float(string="Total Harga Sales", compute="_compute_total_harga")
    produk_kursus_id = fields.Many2one(comodel_name='product.product', string='Produk Kursus', domain=[('is_kursus_product', '=', True)])
    harga_kursus = fields.Float(string='Harga Kursus', related='produk_kursus_id.lst_price')
    pendaftar_ids = fields.One2many(comodel_name='cdn.pendaftaran', inverse_name='kursus_id', string='Pendaftar')
    
    
    
    @api.depends('produk_ids')
    def _compute_total_harga(self):
        for record in self:
            record.total_harga = sum(product.lst_price for product in record.produk_ids)


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
            if not record.instruktur_id:
                raise UserError("Instruktur harus diisi sebelum menghitung jumlah peserta.")
            record.state = "confirm" if record.state == "draft" else record.state

    def action_done(self):
        for record in self:
            record.state = "done" if record.state == "confirm" else record.state

    def action_reset(self):
        for record in self:
            record.state = "draft" 
            
            

            
    
