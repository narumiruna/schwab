from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import SchwabBot


def main():
    dotfile = find_dotenv(raise_error_if_not_found=True)
    print(dotfile)
    load_dotenv()
    SchwabBot.from_env()
