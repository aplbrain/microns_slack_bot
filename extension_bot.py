import logging
import os
import re
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from neuvue_queue_task_assignment.summary_stats.extension.edit_counts import export_edit_counts
from neuvue_queue_task_assignment.summary_stats.extension.task_counts import export_task_counts
from neuvue_queue_task_assignment.summary_stats.extension.task_report import export_task_report
from tabulate import tabulate

CACHE_DAYS = 1
CACHE_DIR = "/home/xenesd1-a/MICRONS/microns_slack_bot/cache"
################ INITIATE BOT #####################################################################

# setting up the environment path
env_path = Path(__file__).parent.resolve() / ".env"
load_dotenv(dotenv_path=env_path)


SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


app = App(token=SLACK_BOT_TOKEN, name='MICrONS Bot')
logger = logging.getLogger(__name__)
help_text = """
1. `edits` - Generate edit counts for all edits and functionally-matched edits.
2. `tasks` - Generate task counts for all enabled namespaces.
    - Single Soma Clean-up
    - Axon on Dendrite/Axon on Axon
    - AGENTS
    - Functional Clean-up
3. `report` - Generate a task report with statistics on tasks, edits, and duration.
4. `help` - Print this help message. 

Make sure  to mention (@) me to run the above commands!
"""
################ FUNCTIONS ########################################################################

def generate_edit_count_table():
    try:
        edits, fm_edits, duration = export_edit_counts()
    except Exception as e:
        return e, -1

    title = f"\nAll Edits as of {datetime.now().strftime('%D')} \n"
    edit_tbl = title + tabulate(edits, headers=edits.columns, tablefmt="simple")

    title = f"\nFunctionally-matched Edits as of {datetime.now().strftime('%D')} \n"
    fm_edit_tbl = title + tabulate(fm_edits, headers=fm_edits.columns, tablefmt="simple")
    
    return f"```{edit_tbl} \n {fm_edit_tbl}```", duration


def generate_task_count_table():
    try:
        tasks, duration = export_task_counts()
    except Exception as e:
        return e, -1
    
    title = f"\nAll Tasks as of {datetime.now().strftime('%D')} \n"
    task_tbl = title + tabulate(tasks, headers=tasks.columns, tablefmt="simple")
    return f"```{task_tbl}```",  duration

def generate_task_report_table():
    try:
        report, duration = export_task_report()
    except Exception as e:
        return e, -1
    
    title = f"\nTask Report as of {datetime.now().strftime('%D')} \n"
    report_tbl = title + tabulate(report, headers=report.columns, tablefmt="simple", maxheadercolwidths=10)
    return f"```{report_tbl}```",  duration

################ APP HOOKS ########################################################################
@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")


@app.event("app_mention")
def give_mention_update(event, say):

    message = event["text"].strip().lower()
    channel = event["channel"]
    user_id = event['user']

    if re.search("(edit)", message):
        say(text="Generating edit counts. Please hold as this takes about 2-10 minutes.", channel=channel)
        response, duration = generate_edit_count_table()
        say(text=response, channel=channel)
        say(text=f"Response Time: {int(duration)} seconds.")
        logger.info(f"Sent edit counts to {user_id}")
    elif re.search("(task)", message):
        say(text="Generating task counts. Please hold as this takes about 1-5 minutes.", channel=channel)
        response, duration = generate_task_count_table()
        say(text=response, channel=channel)
        say(text=f"Response Time: {int(duration)} seconds.")
        logger.info(f"Sent task counts to {user_id}") 
    elif re.search("(report)", message):
        say(text="Generating task report. Please hold as this takes about 1-5 minutes.", channel=channel)
        response, duration = generate_task_report_table()
        say(text=response, channel=channel)
        say(text=f"Response Time: {int(duration)} seconds.")
        logger.info(f"Sent task report to {user_id}") 
    elif re.search("(help)", message):
        say(text=help_text, channel=channel)
        logger.info(f"Sent help prompt to {user_id}")          
    else:
        say(text="I don't recognize that command. Try `help` to see all of the commands I can run!", channel=channel)


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.INFO)
    main()