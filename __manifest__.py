# -*- coding: utf-8 -*-
{
    "name": "aplikasi Kursus",
    "summary": "Aplikasi Manajemen Kursus menggunakan Odoo versi 18",
    "description": """
Long description of module's purpose
    """,
    "author": "Cendana2000",
    "website": "www.cendana2000.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "18.0.0.0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "mail", "product", "account"],
    # always loaded
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/menu_kursus.xml",
        "views/kursus.xml",
        "views/instruktur.xml",
        "views/propinsi.xml",
        "views/kota.xml",
        "views/kecamatan.xml",
        "views/peserta.xml",
        "views/desa.xml",
        "views/training_session.xml",
        "wizards/training_wizard.xml",
        "views/product_inherit.xml",
        "views/pendaftaran.xml",
        "views/kehadiran.xml",
        "reports/action_report.xml",
        "reports/template_report.xml",
        "reports/template_report.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
