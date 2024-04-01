from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import SchwabBot


def main():
    dotfile = find_dotenv()
    print(dotfile)
    load_dotenv()
    SchwabBot.from_env()
