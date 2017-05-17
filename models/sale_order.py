from odoo import models, fields, api, exceptions,_

class CreditLimitAlertSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(CreditLimitAlertSaleOrder, self).action_confirm()

        if self.partner_id.credit != 0:
            if self.partner_id.credit + self.amount_total > self.partner_id.credit_limit:

                raise exceptions.RedirectWarning('Este cliente ha exedido el limite de credito. Su limite actual es: '+ str(self.partner_id.credit_limit) +', actualmente tiene una deuda de: '+ str(self.partner_id.credit) )

        return res