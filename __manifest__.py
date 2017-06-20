{
    'name': 'Credit limit alert',
    'version': '10.0.0',
    'summary': 'Lanza una alerta de limite de credito',
    'description': 'Cuando un vendedor intenta de hacerle una venta a un cliente que ya exedio el limite de credito que tiene aprobado en la empresa, inmediatamente se genera una alerta indicando al vendedor que el cliente exedio su limite',
    'author': 'Raul Ovalle, raul@xmarts.do',
    'website': 'www.xmarts.com',
    'depends': ['sale', 'account_accountant'],
    'data': [
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'reports/partner_statement_report.xml',
    ],
    'installable': True,
}