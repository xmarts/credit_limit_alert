from odoo import models, fields, api

class PosUserReport(models.Model):
    _name = 'report.credit_limit_alert.statement_partner_report'

    @api.multi
    def render_html(self, docids, data):
        """Render report template"""
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('credit_limit_alert.statement_partner_report')

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }

        return report_obj.render('credit_limit_alert.statement_partner_report', docargs)