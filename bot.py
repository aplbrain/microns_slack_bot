import logging
import os
import re
import pyjokes

from dotenv import load_dotenv
from pathlib import Path
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


app = App(token=SLACK_BOT_TOKEN, name='MICrONS Bot')
logger = logging.getLogger(__name__)


@app.message(re.compile("^joke$"))  # type : ignore
def show_random_joke(message, say):
    """Send a random pyjoke back"""
    channel_type = message["channel_type"]
    if channel_type != "im":
        logger.info(f"Channel type is: {channel_type}")
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    logger.info(f"Sent joke < {joke} > to {user_id} ")

    say(text=joke, channel=dm_channel)


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
