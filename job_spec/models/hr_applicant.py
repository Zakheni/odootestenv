# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import rsaidnumber
import PyPDF2
from pypdf import PdfReader
import base64
import io



class Applicant(models.Model):
    _inherit = "hr.applicant"

    # related_applicant_id = fields.Many2one("hr.applicant", string="Related Applicant")
    citizenship = fields.Selection([
        ('SA', 'South Africa'),
        ('other', 'Other')
    ], string='Citizenship', default='other')
    nationality_id = fields.Many2one("res.country", string="Country of Nationality")
    id_no = fields.Char(string="Identification number")
    date_of_birth = fields.Date(string="Date of birth")
    passport = fields.Char(string="Passport")
    #more fields from Zakinfo development
    gender = fields.Selection([('M','Male'),('F','Female')])
    disability =  fields.Selection([('N','No'),('Y','Yes')])
    disability_type = fields.Text(string="Disability Type")
    criminal_record =  fields.Selection([('N','No'),('Y','Yes')])
    crime_info = fields.Text(string="Crime Information")
    mode_of_work =  fields.Selection([('ST','Site'),('OB','Office'), ('both','Both')])
    how_many_years_of_experience = fields.Char(string="How many years of experience")
    notice_period = fields.Text(string="Notice period")
    location = fields.Text(string="Location")
    tell_me_about_your_self = fields.Text(string="1. Tell me about yourself")
    when_can_you_start = fields.Text(string="2. When can you start")
    why_are_you_in_the_job_market_at_the_moment = fields.Text(string="3. Why are you in the job market at the moment")
    how_do_you_feel_about_counter_offer = fields.Text(string="4. How do you feel about counter offer")
    what_are_your_proudest_professional_achievements = fields.Text(string="5. What are your proudest professional achievements")
    #zakinfo developmemt team
    are_you_interviewing_with_other_companies = fields.Text(string="6. Are you interviewing with other companies") 
    when_would_you_be_available_to_start_a_new_role = fields.Text(string="7. When would you be available to start a new role")
    #zakinfo development team - refference check tab1
    reference_Name_and_surname_1 = fields.Text(string="1. Reference Name and surname")
    company_name_1 = fields.Text(string="2. Company Name")
    contact_number_1 = fields.Char(string="3. Contact Number")
    #zakinfo development team - refference check tab2
    reference_Name_and_surname_2 = fields.Text(string="1. Reference Name and surname")
    company_name_2 = fields.Text(string="2. Company Name")
    contact_number_2 = fields.Char(string="3. Contact Number")
    #zakinfo development team - refference check tab3
    reference_Name_and_surname_3 = fields.Text(string="1. Reference Name and surname")
    company_name_3 = fields.Text(string="2. Company Name")
    contact_number_3 = fields.Char(string="3. Contact Number")
    #zakinfo development team - client interview 
    how_do_you_think_the_interview_went = fields.Text(string="1. How do you think the interview went")
    #what_are_your_feelings_regarding_the_organization_and_the_role_now = fields.Text(string="2. What are your feelings regarding the organization & the role now")
    what_type_of_questions_did_the_hiring_manager_ask_you = fields.Text(string="2. What type of questions did the hiring manager ask you")
    what_questions_did_you_ask_at_the_end = fields.Text(string="3. What questions did you ask at the end")
    #zakinfo development team - offer stage
    #the_salary_and_benefit_offer_in_line_with_the_candidate_expectation = fields.Selection([('N','No'),('Y','Yes')])
    did_you_clarify_counter_offer_with_the_candidate = fields.Selection([('N','No'),('Y','Yes')])
    did_the_candidate_accept_the_offer = fields.Selection([('N','No'),('Y','Yes')])
    resume_copy = fields.Binary(string="Resume")

    def create_resume(self):
        for record in self:
            if record.resume_copy:
                pdf_data = base64.b64decode(record.resume_copy)
                reader = PdfReader(io.BytesIO(pdf_data))
                text = ''
                page = reader.pages[0].extract_text()
                # Do something with the extracted text


    @api.onchange("nationality_id")
    def onchange_nationality_id(self):
        if self.nationality_id and self.nationality_id.id == self.env.ref('base.za').id:
            self.citizenship = 'SA'
        else:
            self.citizenship = 'other'

    @api.onchange("id_no")
    def onchange_id_no(self):
        if self.id_no:
            try:
                id_number = rsaidnumber.parse(self.id_no)
                if id_number.valid:
                    self.date_of_birth = id_number.date_of_birth.date()
            except:
                raise UserError("Invalid Identification Number")
        else:
            self.date_of_birth = False

    # def name_get(self):
    #     if self.env.context.get('search_related_applicant'):
    #         result = []
    #         for record in self:
    #             name = ""
    #             if record.partner_name:
    #                 name = "{} [{}]".format(record.partner_name, record.name)
    #             result.append((record.id, name or record.name))
    #         return result
    #     return super(Applicant, self).name_get()

    @api.onchange("partner_name")
    def onchange_related_applicant_id(self):
        if self.partner_name:
            hr_applicant = self.search([('partner_name','=', self.partner_name)], limit=1)
            if hr_applicant:
                self.email_from = hr_applicant.email_from
                self.email_cc = hr_applicant.email_cc
                self.nationality_id = hr_applicant.nationality_id.id
                self.date_of_birth = hr_applicant.date_of_birth
                self.passport = hr_applicant.passport
                #Zakinfo development team
                self.gender = hr_applicant.gender
                self.disability = hr_applicant.disability
                self.criminal_record = hr_applicant.criminal_record
                self.mode_of_work = hr_applicant.mode_of_work
                self.how_many_years_of_experience = hr_applicant.how_many_years_of_experience
                self.notice_period = hr_applicant.notice_period
                self.location = hr_applicant.location

                #Zainfo development team
                self.partner_phone = hr_applicant.partner_phone
                self.partner_mobile = hr_applicant.partner_mobile
                self.linkedin_profile = hr_applicant.linkedin_profile
                self.type_id = hr_applicant.type_id.id
                self.interviewer_ids = [(6, 0, hr_applicant.interviewer_ids.ids)]
                # self.user_id = hr_applicant.user_id.id  # Uncomment if you want to assign user_id
                self.priority = hr_applicant.priority
                self.source_id = hr_applicant.source_id.id
                self.medium_id = hr_applicant.medium_id.id
                self.categ_ids = [(6, 0, hr_applicant.categ_ids.ids)]
                self.job_id = hr_applicant.job_id.id
                self.department_id = hr_applicant.department_id.id
                self.extract_remote_id = hr_applicant.extract_remote_id
                self.salary_expected = hr_applicant.salary_expected
                self.salary_proposed = hr_applicant.salary_proposed
                self.availability = hr_applicant.availability
                self.tell_me_about_your_self = hr_applicant.tell_me_about_your_self
                self.when_can_you_start = hr_applicant.when_can_you_start
                self.why_are_you_in_the_job_market_at_the_moment = hr_applicant.why_are_you_in_the_job_market_at_the_moment
                self.how_do_you_feel_about_counter_offer = hr_applicant.how_do_you_feel_about_counter_offer
                self.what_are_your_proudest_professional_achievements = hr_applicant.what_are_your_proudest_professional_achievements
                # zakinfo development team 
                self.are_you_interviewing_with_other_companies = hr_applicant.are_you_interviewing_with_other_companies
                self.when_would_you_be_available_to_start_a_new_role = hr_applicant.when_would_you_be_available_to_start_a_new_role
                #zainfo development team - reference check tab1
                self.reference_Name_and_surname_1 = hr_applicant.reference_Name_and_surname_1
                self.company_name_1 = hr_applicant.company_name_1
                self.contact_number_1 = hr_applicant.contact_number_1
                #zainfo development team - reference check tab2
                self.reference_Name_and_surname_2 = hr_applicant.reference_Name_and_surname_2
                self.company_name_2 = hr_applicant.company_name_2
                self.contact_number_2 = hr_applicant.contact_number_2
                #zainfo development team - reference check tab3
                self.reference_Name_and_surname_3 = hr_applicant.reference_Name_and_surname_3
                self.company_name_3 = hr_applicant.company_name_3
                self.contact_number_3 = hr_applicant.contact_number_3
                #zakinfo development team - client interview 
                self.how_do_you_think_the_interview_went = hr_applicant.how_do_you_think_the_interview_went
                #self.what_are_your_feelings_regarding_the_organization_and_the_role_now = hr_applicant.what_are_your_feelings_regarding_the_organization_and_the_role_now
                self.what_type_of_questions_did_the_hiring_manager_ask_you = hr_applicant.what_type_of_questions_did_the_hiring_manager_ask_you
                self.what_questions_did_you_ask_at_the_end = hr_applicant.what_questions_did_you_ask_at_the_end
                #zakinfo development team - offer Stage
                #self.the_salary_and_benefit_offer_in_line_with_the_candidate_expectation = hr_applicant.the_salary_and_benefit_offer_in_line_with_the_candidate_expectation
                self.did_you_clarify_counter_offer_with_the_candidate = hr_applicant.did_you_clarify_counter_offer_with_the_candidate
                self.did_the_candidate_accept_the_offer = hr_applicant.did_the_candidate_accept_the_offer

                #             })
