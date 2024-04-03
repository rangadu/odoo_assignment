# -*- coding: utf-8 -*-
import json
from odoo import http, _
from odoo.http import request

from odoo.addons.website.controllers import form


class WebsiteComplaint(http.Controller):

    @http.route(['/complaint_submit'], type='http', auth="public", website=True, sitemap=True)
    def website_complaint_submit(self, **kwargs):
        complaint_types = request.env['complaint.type'].search([], order="id asc")
        return request.render("complaint_management.complaint_submit_form", {'complaint_types': complaint_types})


class WebsiteForm(form.WebsiteForm):

    # Check and insert values from the complaint form on the model complaint.complaint
    def _handle_website_form(self, model_name, **kwargs):
        email = request.params.get('partner_email')

        if email:
            if request.env.user.email == email:
                partner = request.env.user.partner_id
            else:
                # Check is there an contact related to this email address
                partner = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if not partner:
                partner = request.env['res.partner'].sudo().create({
                    'email': email,
                    'name': request.params.get('partner_name', False),
                    'street': request.params.get('street', False),
                    'street2': request.params.get('street2', False),
                    'city': request.params.get('city', False),
                    'lang': request.lang.code,
                })
            request.params['partner_id'] = partner.id
            kwargs.update({'partner_id': partner.id})
            if request.website.complaint_responsible_user_id:
                kwargs.update({'user_id': request.website.complaint_responsible_user_id.id})

        if model_name == 'complaint.complaint':
            kwargs.pop('partner_name', None)
            kwargs.pop('partner_email', None)
            complaint_type = request.params.get('complaint_type_id')

            # Check complaint type is selected or not, if it's not selected it will raise an error message.
            if not complaint_type:
                return json.dumps({
                    'error': _("Complaint Type field is mandatory")
                })

        return super(WebsiteForm, self)._handle_website_form(model_name, **kwargs)

    def insert_attachment(self, model, id_record, files):
        super().insert_attachment(model, id_record, files)
        # If the complaint submit form is submit with attachments,
        # Give access token to these attachments and make the message
        # accessible to the portal user
        # (which will be able to view and download its own documents).
        model_name = model.model
        if model_name == "complaint.complaint":
            complaint = model.env[model_name].browse(id_record)
            attachments = request.env['ir.attachment'].sudo().search([('res_model', '=', model_name), ('res_id', '=', complaint.id), ('access_token', '=', False)])
            attachments.generate_access_token()
            message = complaint.message_ids.filtered(lambda m: m.attachment_ids == attachments)
            message.is_internal = False
            message.subtype_id = request.env.ref('mail.mt_comment')
