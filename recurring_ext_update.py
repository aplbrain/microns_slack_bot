import extension_analysis
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from time import sleep

# setting up the environment path
env_path = Path(__file__).parent.resolve() / ".env"
load_dotenv(dotenv_path=env_path)

time = datetime.now

while True:
    if time().minute % 10 == 0:
        extension_analysis.update_ext_analysis()
    sleep(30)
