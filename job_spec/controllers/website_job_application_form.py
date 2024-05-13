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
from odoo.tools.misc import hmac, consteq

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
                    elif val == 'is_create_resume_from_web' and values[val] == 'on':
                        data.get('record').update({val: True})
                    elif val == 'is_create_resume_from_web' and values[val] == 'on':
                        data.get('record').update({val: False})
                    else:
                        data.get('record').update({val: values[val]})
                if val == 'is_create_resume':
                    data['custom'] = 'create_resume'
        return data

    @http.route('/validate/nationalityId', type='json', auth='public')
    def Validate_nationality_id(self, id_number):
            try:
                id_number = rsaidnumber.parse(id_number)
                if id_number.valid:
                    return True
            except:
                return False

    @http.route('/website/resume/create', type='http', auth="public", methods=['POST'], csrf=False, website=True)
    def job_applicant_resume_create(self, **kwargs):
        if kwargs.get('applicant_id'):
            applicant_id = request.env['hr.applicant'].sudo().browse(int(kwargs.get('applicant_id')))

            # Qualification ids
            qual_dict = {}
            for key, value in kwargs.items():
                if key.startswith(('qualification', 'institute', 'year')):
                    index = key[-1]
                    qual_dict.setdefault(index, {}).update({key[:-1]: value})
            qual_list = [(0, 0, {**value}) for value in qual_dict.values()]

            # Course ids
            course_dict = {}
            for key, value in kwargs.items():
                if key.startswith(('course', 'course_institute')):
                    index = key[-1]
                    course_dict.setdefault(index, {}).update({key[:-1]: value})
            course_list = [(0, 0, {**value}) for value in course_dict.values()]

            # employment History ids
            employment_history_dict = {}
            for key, value in kwargs.items():
                if key.startswith(('emp_company_name', 'emp_date_employed', 'emp_position', 'emp_duties')):
                    index = key[-1]
                    employment_history_dict.setdefault(index, {}).update({key[:-1]: value})
            employment_history_list = [(0, 0, {**value}) for value in employment_history_dict.values()]

            # Skill ids
            skill_dict = {}
            for key, value in kwargs.items():
                if key != 'skills_summary':
                    if key.startswith(('skill', 'skill_experience', 'skill_level')):
                        index = key[-1]
                        skill_dict.setdefault(index, {}).update({key[:-1]: value})
            skill_list = [(0, 0, {**value}) for value in skill_dict.values()]

            # Reference ids
            reference_dict = {}
            for key, value in kwargs.items():
                if key.startswith(('ref_company', 'ref_person', 'ref_person_contact_details')):
                    index = key[-1]
                    reference_dict.setdefault(index, {}).update({key[:-1]: value})
            reference_list = [(0, 0, {**value}) for value in reference_dict.values()]
            values = {k: v for k, v in kwargs.items() if not k[-1].isdigit()}
            values.update({'qualification_ids': qual_list,
                           'course_ids': course_list,
                           'employment_history_ids': employment_history_list,
                           'skill_ids': skill_list,
                           'reference_ids': reference_list,
                           })
            request.env['hr.applicant.resume'].create(values)
            applicant_id.is_create_resume_from_web = False
        return request.render("website_hr_recruitment.thankyou")