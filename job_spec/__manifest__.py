# -*- coding: utf-8 -*-
{
    'name': 'Job Spec (Enterprise)',
    'category': 'Recruitment',
    'summary': 'Recruitment customisation.',
    'description': """
Recruitment customisation
""",
    'author': 'Mayuri Bharadva',
    'version': '16.0.0.1.0',
    'depends': ['hr_recruitment', 'website_hr_recruitment'],
    "data": [
        'security/ir.model.access.csv',
        'views/job_spec.xml',
        'views/hr_applicant_view.xml',
        'views/website_recruitment_templates.xml'
    ],
    'external_dependencies': {
        'python': ['rsaidnumber'],
        # can be install using command "pip install rsa-id-number".
    },
    'assets': {
            'web.assets_frontend': [
                'job_spec/static/src/js/job_application_portal.js',
            ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: