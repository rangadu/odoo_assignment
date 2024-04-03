# -*- coding: utf-8 -*-
from odoo import models, fields


class ComplaintType(models.Model):
    _name = 'complaint.type'

    name = fields.Char(string="Type")
    is_question = fields.Boolean(string="Is a Question?", help="Whether this a question or not")