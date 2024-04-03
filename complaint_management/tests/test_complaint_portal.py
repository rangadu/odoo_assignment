# -*- coding: utf-8 -*-
import re

from odoo import http
from odoo.tests.common import HttpCase, tagged


@tagged('-at_install', 'post_install')
class ComplaintPortal(HttpCase):

    def setUp(self):
        super(ComplaintPortal, self).setUp()
        self.complaint_type = self.env['complaint.type'].create({
            'name': 'Complaint Question',
            'is_question': True
        })

    def test_portal_complaint_submission(self):
        """ Public user should be able to submit a complaint"""
        self.authenticate(None, None)
        complaint_data = {
            'partner_name': 'John Peter',
            'partner_email': 'johnp@example.com',
            'complaint_type_id': self.complaint_type.id,
            'description': 'How can I replace the lamp?',
            'csrf_token': http.Request.csrf_token(self),
        }
        files = [('file', ('test.txt', b'test', 'plain/text'))]
        response = self.url_open('/website/form/complaint.complaint', data=complaint_data, files=files)
        complaint = self.env['complaint.complaint'].browse(response.json().get('id'))
        self.assertTrue(complaint.exists())
        complaint_submitted_response = self.url_open('/complaint-has-been-submitted')
        self.assertEqual(complaint_submitted_response.status_code, 200)
        complaint_submitted_response_complaint_id = (
            re.search(
                rb'Your Complaint Number is #<span>(?P<complaint_id>.*?)</span>',
                complaint_submitted_response.content)
            .group('complaint_id')
        ).decode()
        self.assertIn(
            complaint_submitted_response_complaint_id,
            (complaint.name, str(complaint.id)),
            "Complaint ID on the submitted page does not match with the complaint created"
        )

    def test_portal_complaint_submission_multiple(self):
        REPEAT = 3
        for i in range(REPEAT):
            try:
                self.test_portal_complaint_submission()
            except AssertionError:
                raise AssertionError("Fail on the iteration %s/%s" % (i+1, REPEAT))