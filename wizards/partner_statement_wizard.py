# -*- encoding:utf-8 -*-
from odoo import models, fields, api, tools


class PosOrderLineWizardReport(models.TransientModel):
    """Model for wizard report"""
    _name = 'credit_limit_alert.partner_statement_wizard'
    _description = 'Estado de cuenta de usuarios'

    str_partner_id = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Cliente',compute='_compute_partner')
    date_start = fields.Date('Fecha de inicio')#, required=True)
    date_end = fields.Date('Fecha de fin')#, required=True)


    @api.one
    @api.depends('str_partner_id')
    def _compute_partner(self):
        """
        @api.depends() should contain all fields that will be used in the calculations.
        """
        self.partner_id = self.env['res.partner'].search([('id', '=', self.str_partner_id)])

        pass


    @api.model
    def _get_data(self):


        result = [
            {
            'start': self.date_start,
            'end': self.date_end
            }
        ]

        partner = {
            'name': self.partner_id.name,
            'street': self.partner_id.street,
            'city': self.partner_id.city,
            'state_id': self.partner_id.state_id.name,
            'zip': self.partner_id.zip,
            'country_id':self.partner_id.country_id.name,
            'phone': self.partner_id.phone,
            'email': self.partner_id.email,
            'ref': self.partner_id.ref,
            'property_payment_term_id': self.partner_id.property_payment_term_id.name,
            'credit_limit': self.partner_id.credit_limit,
            'credit_available': self.partner_id.credit_available,
        }
        result.append(partner)


        currency_obj = self.env['res.currency']
        currencys_ids = currency_obj.search([('active', '=', True)])

        for currency in currency_obj.browse(currencys_ids.ids):


            invoices_obj = self.env['account.invoice']
            invoices_ids = invoices_obj.search([
                ('currency_id', '=', currency.id),
                ('partner_id', '=' , self.partner_id.id),
                ('date_invoice', '>=', self.date_start + ' 00:00:00'),
                ('date_invoice', '<=', self.date_end + ' 23:59:59'),
            ], order='date_invoice')

            payments_obj = self.env['account.payment']
            payments_ids = payments_obj.search([
                ('currency_id', '=', currency.id),
                ('partner_id', '=' , self.partner_id.id),
                ('payment_date', '>=', self.date_start + ' 00:00:00'),
                ('payment_date', '<=', self.date_end + ' 23:59:59'),
            ], order='payment_date')

            saldo = 0
            report_lines = []

            for invoice in invoices_ids:
                vals = {
                    'date': invoice.date_invoice,
                    'date_due': invoice.date_due,
                    'move_name': invoice.move_name,
                    'currency_id' : invoice.currency_id.name,
                    'amount_total' : invoice.amount_total,
                    'saldo': saldo,
                    'type': 'invoice',
                }
                report_lines.append(vals)
            for payment in payments_ids:
                pvals = {
                    'date': payment.payment_date,
                    'date_due': '',
                    'move_name': payment.name,
                    'currency_id': payment.currency_id.name,
                    'amount_total': payment.amount,
                    'saldo': saldo,
                    'type': 'payment'
                }
                report_lines.append(pvals)

            sorted_report_lines = sorted(report_lines, key=lambda invoice: invoice['date'])

            for idx, line in enumerate(sorted_report_lines):
                if line['type'] is 'invoice':

                    saldo = saldo + line['amount_total']
                    sorted_report_lines[idx]['saldo'] = saldo

                else:

                    saldo = saldo - line['amount_total']
                    sorted_report_lines[idx]['saldo'] = saldo

            report_currency = {
                'currency': currency.name,
                'saldo': saldo,
                'report_lines':sorted_report_lines,
            }
            if saldo > 0:
                result.append(report_currency)

        return result

    def _build_contexts(self):
        result = {}
        data = self._get_data()
        result['data'] = data

        return result

    def _print_report(self, data):

        return self.env['report'].get_action(self,'credit_limit_alert.statement_partner_report', data=data)

    @api.multi
    def check_report(self):
        self.ensure_one()
        datas = {}
        values = self._build_contexts()

        datas['dates'] = values.get('data').pop(0)
        datas['partner'] = values.get('data').pop(0)
        datas['form'] = values.get('data')

        return self._print_report(datas)




