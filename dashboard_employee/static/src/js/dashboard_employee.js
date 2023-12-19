/** @odoo-module */

import { registry } from "@web/core/registry"
import { useService } from "@web/core/utils/hooks"
const { Component, useRef, onMounted ,useState } = owl

export class EmployeeDashboard extends Component {
    setup(){
        this.state = useState({
            data:{},
            chart:[],
        })
        this.EmployeeLeave = useRef("EmployeeLeave"),
        this.EmployeeExperience = useRef("EmployeeExperience"),
        this.EmployeeAttendance = useRef("EmployeeAttendance"),
        this.EmployeeProjects = useRef("EmployeeProjects"),
        this.EmployeeTasks = useRef("EmployeeTasks"),
        this.EmployeePayslip = useRef("EmployeePayslip"),

        this.orm = useService("orm")

        onMounted(async()=> {
            await this.FetchData();
        })
    }

    async FetchData(){
        this.state.data = await this.orm.call("employee.dashboard", "get_data")
        console.log(this.state.data)
        this.charts(this.EmployeeLeave.el,'line',this.state.data.employee,'Employee Leave',this.state.data.leave_count)
        this.charts(this.EmployeeExperience.el,'line',this.state.data.employee_exp,'Year Of Experience',this.state.data.employee_experience)
        this.charts(this.EmployeeAttendance.el,'pie',this.state.data.attendance_x,'Hours',this.state.data.attendance_y)
        this.charts(this.EmployeeProjects.el,'doughnut',this.state.data.project_x,'Projects',this.state.data.project_y)
        this.charts(this.EmployeeTasks.el,'polarArea',this.state.data.task_x,'Tasks',this.state.data.task_y)
        this.charts(this.EmployeePayslip.el,'bar',this.state.data.payslip_x,'Amount',this.state.data.payslip_y)
    }

    charts(canvas,type,labels,label,data){
        this.state.chart.push(new Chart(
            canvas,
            {
                type:type,
                data: {
                    labels: labels,
                    datasets: [
                        {
                        label: label,
                        data: data,
                        }
                    ]
                },
            }
        ))
    }

}

EmployeeDashboard.template = "EmployeeDashboard"
registry.category("actions").add('employee_dashboard_tags', EmployeeDashboard)
