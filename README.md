# iheartteamwork
Just a bot that loves teamwork.

Currently the bot supports updating time on teamwork. It also can list projects and list tasks by project.


# Installation

Create a bot user on your slack named `iheartteamwork`.
Clone the repo and run the `iheartteamwork.py` script

```
$ git clone https://github.com/syed/iheartteamwork.git
$ cd iheartteamwork
$ python iheartteamwork.py --bot_name=iheartteamwork \
                        --slack_token=<slack token for the bot> \
                        --teamwork_url=<company_name>.teamwork.com \
                        --teamwork_token=<teamwork API token>

```

Once the script starts running. You will see the user `iheartteamwork` online in your slack. 
PM `help` to the bot to give a list of its capabilities.


