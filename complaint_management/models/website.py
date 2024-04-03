# -*- coding: utf-8 -*-
from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    complaint_responsible_user_id = fields.Many2one('res.users', string='Responsible User')
