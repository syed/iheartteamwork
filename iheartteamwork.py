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
	
from slack_api import SlackApi
from teamwork_api import TeamWorkApi
from docopt import docopt


class IHeartTeamwork():


    def __init__(self, bot_name, slack_api_token, teamwork_api_token, teamwork_url):

        self.slack = SlackApi(bot_name, slack_api_token)
        self.tw = TeamWorkApi(teamwork_url, teamwork_api_token)


    def parse_command(self, command, channel_name):
        """
            Main function which gets executed. Will send
            a message that will be posed back to the channel

        """

        out = "YOU DARE SEND ME " + command 
        self.slack.send_message(out, channel_name)

    def start(self):

        self.slack.start_bot(self.parse_command)


if __name__ == "__main__":
   	
    args = docopt(__doc__)
    print args
    iht = IHeartTeamwork(args['--bot_name'], 
                        args['--slack_token'],
                        args['--teamwork_token'],
                        args['--teamwork_url'])

    iht.start()
