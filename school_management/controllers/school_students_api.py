import json
from odoo import api, http, SUPERUSER_ID
from odoo.http import request
from odoo.fields import Date, Datetime


class SchoolStudentsAPI(http.Controller):
    @http.route("/school/api/students", type="http", auth="none", methods=["GET"], csrf=False)
    def get_students(self, **kw):
        env = api.Environment(request.env.cr,SUPERUSER_ID, {})
        students = env['school.student'].sudo().search([])
        student_list = []
        for student in students:
            student_data = {
                'id': student.id,
                'name': student.name,
                'student_id': student.student_id,
                'class_id': student.class_id.name if student.class_id else None,
                'subject_ids': [subject.name for subject in student.subject_ids],
                'gender': student.gender,
                'date_of_birth': Date.to_string(student.date_of_birth) if student.date_of_birth else None,
                'phone': student.phone,
                'email': student.email,
                'address': student.address,
                'active': student.active,
            }
            student_list.append(student_data)
        return request.make_response(
            json.dumps({
                "success": True,
                "data": student_list
            }),headers=[("Content-Type", "application/json")],
        )


    @http.route("/school/api/students/create", type="http", auth="user", methods=["POST"], csrf=False)
    def create_student(self, **kw):
        body = json.loads(request.httprequest.data)
        student = request.env['school.student'].sudo().create(body)
        return request.make_response(
            json.dumps({
                "success": True,
                "data": {
                    'id': student.id,
                    'name': student.name,
                    'student_id': student.student_id,
                    'class_id': student.class_id.name if student.class_id else None,
                    'subject_ids': [subject.name for subject in student.subject_ids],
                    'gender': student.gender,
                    'date_of_birth': Date.to_string(student.date_of_birth) if student.date_of_birth else None,
                    'phone': student.phone,
                    'email': student.email,
                    'address': student.address,
                    'active': student.active,
                }
            }),headers=[("Content-Type", "application/json")],
        )
