# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, _

class HRApplicantResume(models.Model):
    _name = 'hr.applicant.resume'
    _description = 'Zakheni Resume'

    applicant_id = fields.Many2one("hr.applicant")
    surname = fields.Char(string='Surname')
    first_name = fields.Char(string='First Name')
    id_passport = fields.Char(string='ID/Passport')
    languages = fields.Char(string='Languages')
    qualification_ids = fields.One2many('applicant.qualification', 'resume_id', string="Qualifications")
    skills_summary = fields.Text(string='Skills summary')
    additional_comments = fields.Text(string='Additional Comments')
    course_ids = fields.One2many('applicant.course', 'resume_id', string="Courses")
    employment_history_ids = fields.One2many('applicant.employment.history', 'resume_id', string="Employment History")
    skill_ids = fields.One2many('applicant.skill', 'resume_id', string="Skills")
    reference_ids = fields.One2many('applicant.reference', 'resume_id', string="References")



class ApplicantQualification(models.Model):
    _name = 'applicant.qualification'
    _rec_name = 'qualification'

    resume_id = fields.Many2one("hr.applicant.resume")
    qualification = fields.Char("Qualification")
    institute = fields.Char("Institution")
    year = fields.Integer("year")

class ApplicantCourse(models.Model):
    _name = 'applicant.course'
    _rec_name = 'course'

    resume_id = fields.Many2one("hr.applicant.resume")
    course = fields.Char("Course Name")
    course_institute = fields.Char("Institution")

class ApplicantEmploymentHistory(models.Model):
    _name = 'applicant.employment.history'
    _rec_name = 'emp_company_name'

    resume_id = fields.Many2one("hr.applicant.resume")
    emp_company_name = fields.Char("Company")
    emp_date_employed = fields.Char("Employed Dates")
    emp_position = fields.Char("Position")
    emp_duties = fields.Char("Emp Duties")

class ApplicantSkill(models.Model):
    _name = 'applicant.skill'
    _rec_name = 'skill'

    resume_id = fields.Many2one("hr.applicant.resume")
    skill = fields.Char("Skill")
    skill_experience = fields.Char("skill_experience")
    skill_level = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3')
    ], string="Level (1 = Beginner, 2 = Advanced, 3 = Expert)")

class ApplicantReference(models.Model):
    _name = 'applicant.reference'
    _rec_name = 'ref_company'

    resume_id = fields.Many2one("hr.applicant.resume")
    ref_company = fields.Char("Company")
    ref_person = fields.Char("Contact Person")
    ref_person_contact_details = fields.Char("Contact Details")