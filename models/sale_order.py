from odoo import models, fields, api, exceptions,_

class CreditLimitAlertSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    permitted_credit_limit = fields.Boolean('Limite de credito excedido permitido', default=False)

    @api.multi
    def action_confirm(self):

        if self.partner_id.credit_limit != 0:
            if self.partner_id.credit + self.amount_total > self.partner_id.credit_limit:
                if self.payment_term_id.name != 'Immediate Payment':
                    if self.permitted_credit_limit is not True:
                        self.avisado = True
                        raise exceptions.RedirectWarning('Este cliente ha exedido el limite de credito. Su limite actual es: '
                                                         + str(self.partner_id.credit_limit) +', actualmente tiene una deuda de: '
                                                         + str(self.partner_id.credit) + ' y disponible tiene '
                                                         + str(self.partner_id.credit_available)
                                                         + ', debe que autorizar el limite de credito excedido' )

        res = super(CreditLimitAlertSaleOrder, self).action_confirm()

        return res