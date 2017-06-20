from odoo import models, fields, api

class CreditLimitAlertResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    credit_limit = fields.Monetary('Limite de credito')
    credit_available = fields.Monetary('Cedito disponible', compute='_compute_amount_credit_available')
    # date_start = fields.Date('Fecha de inicio', required=True)
    # date_end = fields.Date('Fecha de fin', required=True)
    #
    # @api.one
    # @api.depends('credit_limit','credit_available','credit')
    # def _compute_amount_credit_available(self):
    #
    #     self.credit_available = self.credit_limit - self.credit
    #
    #     pass
    #
    #
    # @api.model
    # def _get_data(self):
    #     invoices_obj = self.env['account.invoice']
    #     invoices_ids = invoices_obj.search([
    #         ('date_invoice', '>=', self.date_start + ' 00:00:00'),
    #         ('date_invoice', '<=', self.date_end + ' 23:59:59')
    #     ])
    #
    #     result = [{'start': self.date_start, 'end': self.date_end}]
    #
    #     for invoice in invoices_obj.browse(invoices_ids.ids):
    #         vals = {
    #             'name': invoice.name
    #         }
    #         result.append(vals)
    #
    #     return result
    #
    # def _build_contexts(self):
    #     result = {}
    #     data = self._get_data()
    #     result['data'] = data
    #
    #     return result
    #
    # def _print_report(self, data):
    #
    #     return self.env['report'].get_action(self,'credit_limit_alert.statement_partner_report', data=data)
    #
    # @api.multi
    # def check_report(self):
    #     self.ensure_one()
    #     datas = {}
    #     values = self._build_contexts()
    #
    #     datas['dates'] = values.get('data').pop(0)
    #     datas['form'] = values.get('data')
    #
    #     return self._print_report(datas)




