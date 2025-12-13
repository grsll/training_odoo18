from odoo import models, fields, api


class Propinsi(models.Model):
    _name = "cdn.propinsi"
    _description = "Referensi Propinsi"

    kode = fields.Char(string="kode", required=True)
    name = fields.Char(string="Nama Propinsi", required=True, help="")
    singkatan = fields.Char(string="Singkatan", help="")
    description = fields.Text(string="Deskripsi", help="")

    kota_ids = fields.One2many(
        comodel_name="cdn.kota", inverse_name="propinsi_id", string="Kota", help=""
    )


class Kota(models.Model):
    _name = "cdn.kota"
    _description = "Referensi Kota"

    name = fields.Char(string="Nama Kota", required=True, help="")
    kode = fields.Char(string="Kode", required=True)

    singkatan = fields.Char(string="Singkatan", help="")
    description = fields.Text(string="Deskripsi", help="")

    propinsi_id = fields.Many2one(
        comodel_name="cdn.propinsi", string="Propinsi", help=""
    )
    kecamatan_ids = fields.One2many(
        comodel_name="cdn.kecamatan",
        inverse_name="kota_id",
        string="Kecamatan",
        help="",
    )


class Kecamatan(models.Model):
    _name = "cdn.kecamatan"
    _description = "Referensi Data Kecamatan"

    name = fields.Char(string="Nama Kecamatan", required=True, help="")
    kode = fields.Char(string="Kode")

    description = fields.Text(string="Deskripsi", help="")

    kota_id = fields.Many2one(comodel_name="cdn.kota", string="Kota", help="")
    desa_ids = fields.One2many(
        comodel_name="cdn.desa",
        inverse_name="kecamatan_id",
        string="Desa/Kelurahan",
        help="",
    )


class Desa(models.Model):
    _name = "cdn.desa"
    _description = "Referensi Data Desa/Kelurahan"

    name = fields.Char(string="Nama Desa/Kelurahan", required=True, help="")
    kode = fields.Char(string="Kode", required=True)

    description = fields.Text(string="Deskripsi", help="")
    kecamatan_id = fields.Many2one(
        comodel_name="cdn.kecamatan", string="Kecamatan", help=""
    )
