import base64
import json

from markupsafe import escape
from psycopg2 import IntegrityError
from werkzeug.exceptions import BadRequest

from odoo import http, SUPERUSER_ID, _, _lt
from odoo.http import request
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.exceptions import AccessDenied, ValidationError, UserError
import rsaidnumber

class WebsiteFormInherit(WebsiteForm):

    def extract_data(self, model, values):
        data = super(WebsiteFormInherit, self).extract_data(model=model, values=values)
        if model.name == 'Applicant':
            data['custom'] = ''
            fields_list = request.env['hr.applicant']._fields.keys()
            for val in values:
                if val in fields_list:
                    if val == 'citizenship' and values['citizenship'] == 'SA':
                        id_number = rsaidnumber.parse(values['id_no'])
                        data.get('record').update({'nationality_id': request.env.ref('base.za').id,
                                                   'date_of_birth': id_number.date_of_birth})
                    data.get('record').update({val: values[val]})
        return data

    @http.route('/validate/nationalityId', type='json', auth='public')
    def Validate_nationality_id(self, id_number):
            try:
                id_number = rsaidnumber.parse(id_number)
                if id_number.valid:
                    return True
            except:
                return False