from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import SchwabBot


def main():
    load_dotenv(find_dotenv(usecwd=True))
    SchwabBot.from_env()
