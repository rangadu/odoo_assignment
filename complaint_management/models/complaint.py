# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from odoo.tools.misc import format_date
from odoo.exceptions import ValidationError


class ComplaintComplaint(models.Model):
    _name = 'complaint.complaint'
    _description = 'Complaint'
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]

    name = fields.Char(string="Name", required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string="Customer")
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string="Assigned To", tracking=True)
    complaint_type_id = fields.Many2one('complaint.type', string="Complaint Type")
    is_question = fields.Boolean(related="complaint_type_id.is_question")
    description = fields.Text(string="Complaint")
    action_plan = fields.Html(string="Action Plan")
    state = fields.Selection([('new', 'New'),
                              ('in_review', 'In Review'),
                              ('in_progress', 'In Progress'),
                              ('solved', 'Solved'),
                              ('dropped', 'Dropped'),
                              ], string="Stage", tracking=True, default='new')
    answer = fields.Html(string="Answer")
    submit_date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())
    close_date = fields.Datetime(string="Close Date", tracking=True)
    l10n_din5008_template_data = fields.Binary(compute='_compute_l10n_din5008_template_data')
    l10n_din5008_document_title = fields.Char(compute='_compute_l10n_din5008_document_title')
    l10n_din5008_addresses = fields.Binary(compute='_compute_l10n_din5008_addresses', exportable=False)

    # Compute template data for din5008 compatible work order report
    def _compute_l10n_din5008_template_data(self):
        for record in self:
            record.l10n_din5008_template_data = data = []
            if record.name:
                data.append((_("Complaint No"), record.name))
            if record.partner_id:
                data.append((_("Responsible"), record.user_id.name))
            if record.submit_date:
                data.append((_("Submit Date"), format_date(self.env, record.submit_date)))

    def _compute_l10n_din5008_document_title(self):
        for record in self:
                record.l10n_din5008_document_title = _("Work Order")

    def _compute_l10n_din5008_addresses(self):
        for record in self:
            record.l10n_din5008_addresses = data = []
            if record.partner_id:
                data.append((_('Customer Address:'), record.partner_id))

    @api.model_create_multi
    def create(self, vals_list):
        template = self.env.ref('complaint_management.complaint_request_email_template')
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('complaint.complaint') or _("New")
        ticket = super(ComplaintComplaint, self).create(vals_list)
        ticket.send_email(template)
        return ticket

    def action_in_review(self):
        self.write({'state': 'in_review'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_solve(self):
        """
            Before close the complaint ticket, it's checking action plan field is filled or not. if not it will raise an error
            If it's a question, user will be able to close the complaint ticket without filling the action plan.
            But user needs to fill the answer field.
        """

        template = self.env.ref('complaint_management.complaint_close_email_template')

        if self.complaint_type_id.is_question:
            if self.answer:
                self.write({'state': 'solved', 'close_date': fields.Datetime.now()})
                self.send_email(template)
            else:
                raise ValidationError(_("Please, write down the answer and close the complaint ticket."))
        else:
            if self.action_plan:
                self.write({'state': 'solved', 'close_date': fields.Datetime.now()})
                self.send_email(template)
            else:
                raise ValidationError(_("Please, write down the action plan and close the complaint ticket."))

    def action_drop(self):
        template = self.env.ref('complaint_management.complaint_close_email_template')

        self.write({'state': 'dropped', 'close_date': fields.Datetime.now()})
        self.send_email(template)

    # After creation of the complaint, it will send an email to customer with the complaint details
    def send_email(self, template):
        for rec in self:
            if template:
                template.send_mail(rec.id)

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'Complaint Work Order-%s' % (self.name)
