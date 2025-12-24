from odoo import models, fields, api


class Pendaftaran(models.Model):
    _name = "cdn.pendaftaran"
    _description = "Tabel Pendaftaran"

    name = fields.Char(string="Nomor Pendaftaran", readonly=True)
    tanggal = fields.Date(string="Tanggal", default=fields.Date.today(), required=True)
    pendaftar_id = fields.Many2one(
        comodel_name="cdn.peserta", string="Peserta Kursus", required=True
    )
    jenis_kelamin = fields.Selection(
        string="Jenis Kelamin", related="pendaftar_id.jenis_kelamin"
    )
    no_hp = fields.Char(string="No HP", related="pendaftar_id.mobile")
    kursus_id = fields.Many2one(
        comodel_name="cdn.kursus", string="Kursus", required=True
    )
    harga_kursus = fields.Float(string="Harga Kursus", related="kursus_id.harga_kursus")
    state = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Konfirmasi"),
        ],
        default="draft",
    )
    invoice_id = fields.Many2one(comodel_name="account.move", string="No Tagihan", readonly=True)
    status_pembayaran = fields.Selection(string="Status Pembayaran", related="invoice_id.status_in_payment")

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code("cdn.pendaftaran")
        return super(Pendaftaran, self).create(vals)

    def action_set_draft(self):
        for record in self:
            record.state = "draft"

    def action_confirm(self):
        for record in self:
            record.state = "confirm"

    def action_create_invoice(self):
        Invoice = self.env["account.move"]
        for record in self:
            invoice_vals = {
                "move_type": "out_invoice",
                "partner_id": record.pendaftar_id.partner_id.id,
                "invoice_date": record.tanggal,
                "invoice_line_ids": [
                    (0, 0, {
                            "name": record.kursus_id.name,
                            "product_id": record.kursus_id.produk_kursus_id.id,
                            "quantity": 1,
                            "price_unit": record.harga_kursus,
                        },
                    )
                ],
            }
            invoice = Invoice.create(invoice_vals)
            record.invoice_id = invoice.id
            invoice.action_post()
