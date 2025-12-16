from odoo import models, fields, api


class WizardTraining(models.TransientModel):
    _name = "cdn.wizard.training"
    _description = "Cep Wizard Training"

    def _default_sesi(self):
        return self.env["cdn.training.session"].browse(self._context.get("active_ids"))

    session_id = fields.Many2one(comodel_name="cdn.training.session", string="Sesi Training", default=_default_sesi)
    peserta_ids = fields.Many2many(comodel_name="cdn.peserta", string="Peserta Training")

    def tambah_peserta(self):
        self.session_id.peserta_ids |= self.peserta_ids
        
    session_ids = fields.Many2many(comodel_name='cdn.training.session', string='Multi Sesi Training', default=_default_sesi)
    
    def tambah_banyak_peserta(self):
        for session in self.session_ids:
            session.peserta_ids |= self.peserta_ids

