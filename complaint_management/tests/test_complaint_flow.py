# -*- coding: utf-8 -*-
from .common import ComplaintCommon


class TestComplaintFlow(ComplaintCommon):
    """ Test used to check that the base functionalities of complaint backend function as expected.
        - test_complaint_user: Check default user is set during the complaint creation
        - test_normal_type_complaint: Check normal type complaint work flow
        - test_question_type_complaint: Check question type complaint work flow
    """

    @classmethod
    def setUpClass(cls):
        res = super().setUpClass()
        return res

    def test_complaint_user(self):
        # Create a partner
        partner = self.env['res.partner'].create({
            'name': 'John Peter'
        })
        # complaint responsible user create a complaint for the partner
        complaint = self.env['complaint.complaint'].create({
            'name': 'CC001',
            'partner_id': partner.id,
            'complaint_type_id': self.type_question.id,
            'user_id': self.complaint_responsible.id
        })
        self.assertTrue(complaint.user_id.id != False, "Responsible user should automatically assigned based on the configurations")

    def test_normal_type_complaint(self):
        # Create a partner
        partner = self.env['res.partner'].create({
            'name': 'John Peter'
        })

        # Create a normal type complaint
        complaint = self.env['complaint.complaint'].create({
            'name': 'CC002',
            'partner_id': partner.id,
            'complaint_type_id': self.type_issue.id,
            'description': 'Wall lamp not working',
            'action_plan': "Test Plan",
            'is_question': False,
            'user_id': self.complaint_responsible.id
        })
        complaint.action_solve()
        self.assertEqual(complaint.state, 'solved')

    def test_question_type_complaint(self):
        # Create a partner
        partner = self.env['res.partner'].create({
            'name': 'John Peter'
        })

        # Create a normal type complaint
        complaint = self.env['complaint.complaint'].create({
            'name': 'CC003',
            'partner_id': partner.id,
            'complaint_type_id': self.type_issue.id,
            'action_plan': "Site Visit",
            'description': 'How can I replace the lamp?',
            'answer': "Test Answer",
            'user_id': self.complaint_responsible.id
        })
        complaint.action_solve()
        self.assertEqual(complaint.state, 'solved')
