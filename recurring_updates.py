import final_bot
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from time import sleep

# setting up the environment path
env_path = Path(__file__).parent.resolve() / ".env"
load_dotenv(dotenv_path=env_path)

# the channel to send updates to
# channel_id = " C03QE4QBA3E"

time = datetime.now

while True:
    if time().hour == 11 and time().minute == 59:
        final_bot.send_scheduled_update()
    sleep(60)
