import time
from slackclient import SlackClient

class SlackApi:
    def __init__(self, bot_name, api_token):
        # instantiate Slack & Twilio clients
        self.bot_name = bot_name
        self.slack_client = SlackClient(api_token)
        self.bot_id = self._get_bot_id()
        self.AT_BOT = "<@" + self.bot_id + ">"

    def _get_bot_id(self):
        api_call = self.slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == self.bot_name:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                    return user.get('id')
        else:
            raise Exception("could not find bot user with the name " + BOT_NAME)

    def parse_slack_output(self, slack_rtm_output):
        """
            The Slack Real Time Messaging API is an events firehose.
            this parsing function returns None unless a message is
            directed at the Bot, based on its ID.
        """

        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                # print output
                if output and 'text' in output and 'user' in output and output['user'] != self.bot_id:
                    # return text after the @ mention, whitespace removed
                    return output['text'].strip(), output['user']

        return None, None

    def send_message(self, message, channel):
        self.slack_client.api_call("chat.postMessage", channel=channel,
                                   text=message, as_user=True)

    def start_bot(self, callback_fn):
        READ_WEBSOCKET_DELAY = 0.5  # 1 second delay between reading from firehose
        if self.slack_client.rtm_connect():
            print("Teamworker connected and running!")
            while True:
                command, channel = self.parse_slack_output(self.slack_client.rtm_read())
                if command and channel:
                    callback_fn(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
