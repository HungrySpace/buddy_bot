import os
from dotenv import load_dotenv, find_dotenv

# Loading .env variables
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = "1764514462:AAEEjdaLB_2GpZcDSKh7p7RtgiZ-7A5sn3Y"# os.getenv("TELEGRAM_TOKEN")

if TELEGRAM_TOKEN is None:
    raise Exception("Please setup the .env variable TELEGRAM_TOKEN.")

PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")


WELCOME_MESSAGE = os.getenv("WELCOME_MESSAGE", "👋")
