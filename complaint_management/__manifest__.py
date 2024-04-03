# -*- coding: utf-8 -*-
{
    'name': "Complaint Management",
    'version': '17.0.1.0.1',
    'author': "Ranga Dharmapriya",
    'maintainer': "Ranga Dharmapriya",
    'category': 'Website',
    'summary': 'Website Complaint Submit Form',
    'description': """
=====================
Complaint Management
=====================
This module is designed to facilitate the process of submitting complaints regarding rented flats for tenants of 
RealEstateX properties. This module integrates seamlessly into RealEstateX's existing Odoo system, providing a 
user-friendly interface for tenants to submit complaints, which are then efficiently managed and addressed 
by RealEstateX's employees.
    """,
    'depends': ['website', 'l10n_din5008'],
    'data': [
        'security/ir.model.access.csv',

        'report/complaint_report_templates.xml',
        'report/ir_actions_report.xml',

        'data/ir_sequence_data.xml',
        'data/complaint_data.xml',
        'data/mail_template_data.xml',

        'views/complaint_views.xml',
        'views/complaint_type_views.xml',
        'views/complaint_management_menus.xml',
        'views/res_config_settings_views.xml',
        'views/complaint_templates.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
}