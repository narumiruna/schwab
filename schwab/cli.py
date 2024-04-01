from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import SchwabBot


def main():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    SchwabBot.from_env()
