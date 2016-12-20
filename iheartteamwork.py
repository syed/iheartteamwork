"""
I am a bot that loves teamwork

Usage:
	iheartteamwork.py --bot_name=<bot_name> --slack_token=<slack_token> 
			 --teamwork_url=<teamwork_url> --teamwork_token=<teamwork_token>

Options:

	-h --help				Show help
	--bot_name=<bot_name>			Name of the bot
 	--slack_token=<slack_token> 		Slack API token
	--teamwork_url=<teamwork_url> 		Teamwork URL like 'cloudops.teamwork.com'
	--teamwork_token=<teamwork_token>	Teamwork API token	

"""
import pprint
import re
import shlex
from datetime import timedelta, datetime
from docopt import docopt

from slack_api import SlackApi
from teamwork_api import TeamWorkApi

HELP_TEXT = """
```
update project:<project-name> task:<task-name> date:<YYYY-MM-DD> duration:<time in hrs> billable:true user:<emailid>
show projects
show projects like <keyword>
show tasks <project_name>

Example:

    update project:CloudOps task:ACS date:2016-01-01 duration:8 billable:true user:sahmed@cloudops.com

```
"""

class IHeartTeamwork:
    COMMANDS = ['help', 'update-time']

    def __init__(self, bot_name, slack_api_token, teamwork_api_token, teamwork_url):

        self.slack = SlackApi(bot_name, slack_api_token)
        self.tw = TeamWorkApi(teamwork_url, teamwork_api_token)

    def execute_help(self):
        return HELP_TEXT

    def execute_show_projects(self, keyword=None):
        return "```" + '\n'.join([x.get('name') for x in self.tw.list_projects()]) + "```"

    def execute_show_tasks(self, project_name):
        project_id = self._get_project_id(project_name)

        if not project_id:
            return "No project %s found " % project_name

        return "```" + '\n'.join([x.get('content') for x in self.tw.get_project_tasks(project_id)]) + "```"

    def parse_args(self, items):

        args = {}
        for item in items:
            kv = item.split(':')
            if len(kv) > 1:
                args[kv[0].lower().strip()] = kv[1].strip()

        return args

    def execute_update_time(self, args):

        print args

        try:
            args = self.validate_and_update_time_args(args)
        except ValueError as e:
            return str(e)

        pprint.pprint(args)

        self.tw.save_task_time(args['task_id'], args['datetime_date'], args['duration'],
                       args['user_id'] , args['description'] , args['datetime_date'], args['billable'])


        return "Updated time"

    def validate_and_update_time_args(self, args):

        mandatory_params = ['project', 'task', 'date', 'duration', 'user', 'billable', 'description']
        for param in mandatory_params:
            if param not in args:
                raise ValueError("%s parameter not found, see help" % param)

        project_name = args['project']
        project_id = self._get_project_id(project_name)
        print project_id
        if not project_id:
            raise ValueError("project %s not found, check the project name" % project_name)

        task_name = args['task']
        task_id = self._get_task_id(project_id, task_name)

        if not task_id:
            raise ValueError("task %s not found, check the task name" % task_name)

        if not self._is_int(args['duration']):
            raise ValueError("duration should be an int")

        datetime_date = self._get_datetime(args['date'])
        if not datetime_date:
            raise ValueError("date must be of the form YYYY-MM-DD")

        user_name = args['user']
        user_id = self._get_user_id(user_name)
        if not user_id:
            raise ValueError("User not found, check the username")

        if args['billable'].lower() not in ['true', 'false']:
            raise ValueError("Possible values for billable: true, false")

        args['billable'] = args['billable'].lower() == 'true'
        args['project_id'] = project_id
        args['task_id'] = task_id
        args['user_id'] = user_id
        args['datetime_date'] = datetime_date
        args['duration'] = timedelta(hours=int(args['duration']))

        return args

    def _get_datetime(self, date_str):

        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None

    def _is_int(self, val):
        try:
            x = int(val)
        except ValueError:
            return False
        return True

    def parse_slack_command(self, command, channel_name):
        """
        Main function which gets executed. Will send
        a message that will be posed back to the channel

        """

        command = self._clean_string(command)
        items = shlex.split(command)
        print items
        
        if command.startswith('help'):
            response = self.execute_help()
        elif command.startswith('update'):
            args = self.parse_args(items)
            response = self.execute_update_time(args)
        elif command.startswith('show projects'):
            args = self.parse_args(items)
            response = self.execute_show_projects()
        elif command.startswith('show tasks'):
            args = self.parse_args(items)
            response = self.execute_show_tasks(items[2])
        else:
            response = self.execute_help()

        self.slack.send_message(response, channel_name)

    def _clean_string(self, data):
        return re.sub("<.+?\|(.+?)>", "\\1", data)

    def _get_project_id(self, project_name):
        projects = self.tw.list_projects()

        for project in projects:
            if project.get('name') == project_name:
                return int(project.get('id'))
        return None

    def _get_task_id(self, project_id, task_name):
        tasks = self.tw.get_project_tasks(project_id)

        for task in tasks:
            print task.get('content')
            if task.get('content') == task_name:
                return int(task.get('id'))

        return None

    def _get_user_id(self, user_name):
        users = self.tw.list_users()
        for user in users:
            if user.get('email-address') == user_name:
                return int(user.get('id'))

        return None

    def start(self):
        self.slack.start_bot(self.parse_slack_command)


if __name__ == "__main__":
    args = docopt(__doc__)
    print args
    iht = IHeartTeamwork(args['--bot_name'],
                         args['--slack_token'],
                         args['--teamwork_token'],
                         args['--teamwork_url'])

    iht.start()
