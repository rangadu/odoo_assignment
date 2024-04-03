# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    complaint_responsible_user_id = fields.Many2one('res.users', related='website_id.complaint_responsible_user_id', string='Responsible User', readonly=False, domain="[('share', '=', False)]")
