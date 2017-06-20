# -*- encoding:utf-8 -*-
from openerp import models, fields, api, tools


class PosOrderLineWizardReport(models.TransientModel):
    """Model for wizard report"""
    _name = 'credit_limit_alert.partner_statement_wizard'
    _description = 'Estadod e cuenta de usuarios'

    partner_id = fields.Many2one('res.partner', 'Cliente')
    date_start = fields.Date('Fecha de inicio', required=True)
    date_end = fields.Date('Fecha de fin', required=True)

    @api.model
    def _get_data(self):

        invoices_obj = self.env['account.invoice']
        invoices_ids = invoices_obj.search([
            ('date_invoice', '>=', self.date_start + ' 00:00:00'),
            ('date_invoice', '<=', self.date_end + ' 23:59:59')
        ])

        result = [{'start': self.date_start, 'end': self.date_end}]


        for invoice in invoices_obj.browse(invoices_ids.ids):
            vals = {
                'name': invoice.name
            }
            result.append(vals)

        return result

    def _build_contexts(self):
        result = {}
        data = self._get_data()
        result['data'] = data

        return result

    def _print_report(self, data):
        return self.pool['report'].get_action(
            'pos_user_report.report_pos_order', data=data)


    @api.multi
    def check_report(self):
        self.ensure_one()
        datas = {}
        values = self._build_contexts()

        datas['dates'] = values.get('data').pop(0)
        datas['form'] = values.get('data')

        return self._print_report(datas)



