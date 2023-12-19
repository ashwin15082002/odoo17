# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, models
from odoo.fields import Date


class EmployeeDashboard(models.Model):
    _name = 'employee.dashboard'

    @api.model
    def get_datas(self, date):
        """ This function is used to get datas for chart and return the datas into dashboard_employee.js file"""
        date_count = date
        end_date = Date.today()
        if date_count == '30':
            start_date = end_date - timedelta(days=30)
            res = self.get_data(start_date)
            return res
        else:
            start_date = end_date - timedelta(days=7)
            res = self.get_data(start_date)
            return res

    def get_data(self, start_date):
        user = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])

        # get employee leave data

        leaves = self.env['hr.leave'].search([('date_from', '>', start_date)])
        employee_leave = []
        employee_leave_count = []
        for employee in leaves:
            employee_leave.append(employee.employee_id.name)
            employee_leave_count.append(employee.number_of_days)

        # get employee experience data

        employee_exp = []
        employee_experience = []
        experience = self.env['hr.employee'].search([])
        for exp in experience:
            employee_exp.append(exp.name)
            employee_experience.append(Date.today().year - exp.create_date.date().year)

        # get employee attendance data

        attendance = self.env['hr.attendance'].sudo().search([]).filtered(lambda x: x.check_in.date() > start_date)
        attendance_employee = list(set([record.employee_id.name
                                        for record in attendance]))

        work_hours = []
        for record in attendance_employee:
            total_hour = 0
            for rec in attendance:
                if record == rec.employee_id.name:
                    total_hour += rec.worked_hours
            work_hours.append(total_hour)

        # get employee project data

        project = self.env['project.project'].sudo().search([('date_start', '>', start_date)])
        project_manager = list(set([pro.user_id.name for pro in project]))
        project_count = []
        for record in project_manager:
            count = 0
            for rec in project:
                if record == rec.user_id.name:
                    count += 1
            project_count.append(count)

        # get employee task data

        tasks = self.env['project.task'].sudo().search([])
        projects = [pro.name for pro in project]
        tasks_count = []
        for project in projects:
            count = 0
            for task in tasks:
                if task.project_id.name == project:
                    count += 1
            tasks_count.append(count)

        # get employee payslip data

        payslips = self.env['hr.payslip'].sudo().search([]).filtered(lambda x: x.create_date.date() > start_date)
        payslip_employee = list(set([rec.employee_id.name for rec in payslips]))

        payslip_line = [self.env['hr.payslip.line'].sudo().search([
            ('slip_id', '=', record.id), ('code', '=', 'NET')]) for record in payslips]
        payslip_y = []
        for record in payslip_employee:
            amount = 0
            for rec in payslip_line:
                if record == rec.employee_id.name:
                    amount += rec.amount
            payslip_y.append(amount)

        # returning datas

        records = {
            'employee': employee_leave,
            'leave_count': employee_leave_count,

            'employee_exp': employee_exp,
            'employee_experience': employee_experience,

            'attendance_x': attendance_employee,
            'attendance_y': work_hours,

            'project_x': project_manager,
            'project_y': project_count,

            'payslip_x': payslip_employee,
            'payslip_y': payslip_y,

            'task_x': projects,
            'task_y': tasks_count,


            'name': user.name,
            'department': user.department_id.name,
            'phone': user.work_phone,
            'email': user.work_email,
            'job': user.job_title,
        }
        return records
