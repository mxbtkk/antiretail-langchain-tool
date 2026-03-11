import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()
ANTI_RETAIL_API_KEY = os.getenv("ANTI_RETAIL_API_KEY")
BASE_URL = "https://api.tradingdatapro.com"

@tool
def get_anti_retail_signals(asset: str = None) -> str:
    """
    Fetches anti-retail crypto market signals for BTC or ETH.
    Provides insights into crowded trades, options sentiment, and volatility.
    Returns a summary of market conditions and strategic recommendations.

    Args:
        asset (str, optional): The cryptocurrency asset to get signals for (e.g., "BTC", "ETH").
                                If None, fetches a general market overview.
    """
    headers = {"x-api-key": ANTI_RETAIL_API_KEY}
    endpoint = f"{BASE_URL}/api/signals" if asset is None else f"{BASE_URL}/api/signals?asset={asset}"

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching anti-retail signals: {e}"

# Example of how an agent might use this tool (more complex logic in agent itself)
if __name__ == "__main__":
    # This part is for demonstration/testing the tool in isolation
    # An actual LangChain agent would call get_anti_retail_signals(asset="BTC")
    print(get_anti_retail_signals(asset="BTC"))
    print(get_anti_retail_signals(asset="ETH"))
    print(get_anti_retail_signals())
