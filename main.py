from dotenv import find_dotenv
from dotenv import load_dotenv

from schwab.client import Client


def main() -> None:
    load_dotenv(find_dotenv())

    client = Client.from_env()

    resp = client.query_quotes(symbols=["AAPL", "GBP/USD"])
    print(resp)


if __name__ == "__main__":
    main()
