from odoo import models, fields, api

class CreditLimitAlertResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    credit_limit = fields.Monetary('Limite de credito')
    credit_available = fields.Monetary('Cedito disponible', compute='_compute_amount_credit_available')

    @api.one
    @api.depends('credit_limit','credit_available','credit')
    def _compute_amount_credit_available(self):

        self.credit_available = self.credit_limit - self.credit

        pass
