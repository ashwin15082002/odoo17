# -*- coding: utf-8 -*-

{
    'name': "Dashboard Employee",
    'version': '17.0.1.0.0',
    'depends': ['base','hr','board','project'],
    'author': "Ashwin",
    'category': 'category',
    'description': """  """,
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    # data files always loaded at installation
    'data': [
        'data/dashboard_employee.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',
            'dashboard_employee/static/src/xml/employee_dashboard.xml',
            'dashboard_employee/static/src/js/dashboard_employee.js',

        ]
    }
}
