# -*- coding: utf-8 -*-
from odoo.addons.mail.tests.common import MockEmail
from odoo.tests.common import TransactionCase


class ComplaintCommon(TransactionCase, MockEmail):

    @classmethod
    def setUpClass(cls):
        super(ComplaintCommon, cls).setUpClass()
        cls._init_mail_gateway()

        # create a complaint responsible  user
        Users = cls.env['res.users'].with_context(tracking_disable=True)
        cls.main_company_id = cls.env.user.company_id.id
        cls.partner = cls.env['res.partner'].create({
            'name': 'Customer Support'
        })

        cls.complaint_responsible = Users.create({
            'company_id': cls.main_company_id,
            'name': 'User',
            'login': 'user',
            'email': 'user@example.com',
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id])],
            'tz': 'Europe/Brussels',
        })

        # He also creates a ticket types for Question and Issue
        cls.type_question = cls.env['complaint.type'].with_user(cls.complaint_responsible).create({
            'name': 'Complaint Test',
            'is_question': True
        }).sudo()
        cls.type_issue = cls.env['complaint.type'].with_user(cls.complaint_responsible).create({
            'name': 'Complaint Question',
            'is_question': False
        }).sudo()

    def flush_tracking(self):
        """ Force the creation of tracking values. """
        self.env.flush_all()
        self.cr.flush()
