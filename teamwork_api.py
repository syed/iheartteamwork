import teamwork
import pprint
import sys

import datetime

class TeamWorkApi():

    def __init__(self, company, api_key):
        self.instance = teamwork.Teamwork(company, api_key)

    def list_projects(self):
        return self.instance.get_projects()

    def list_users(self):
        return self.instance.get_people()

    
    def get_project_tasks(self, project_id):
        return self.instance.get_project_tasks(project_id)

    def save_task_time(self, task_id, entry_date, duration,
                        user_id, description, start_time, is_billable):

        self.instance.save_task_time_entry(task_id, entry_date, duration,
                user_id, description, start_time, False)

