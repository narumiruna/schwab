from dotenv import find_dotenv
from dotenv import load_dotenv

from schwab.client import Client
from schwab.quote import QuoteRequest


def main() -> None:
    load_dotenv(find_dotenv())

    client = Client.from_env()
    client.refresh_token()

    req = QuoteRequest(symbols=["AAPL", "GBP/USD"])
    resp = client.get_quote(req)
    print(resp)


if __name__ == "__main__":
    main()
