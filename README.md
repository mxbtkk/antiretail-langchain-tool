# Anti-Retail Crypto API LangChain Tool

This repository demonstrates how to integrate the [Anti-Retail Crypto Data API](https://api.tradingdatapro.com) as a custom tool within LangChain agents.

The Anti-Retail Crypto Data API provides real-time derivatives intelligence for Bitcoin (BTC) and Ethereum (ETH), combining futures data from 12+ exchanges with Deribit options analytics. It offers pre-computed anti-retail signals to identify crowded trades, smart money positioning, volatility regimes, and market bias.

## API Endpoints

- **Base URL:** `https://api.tradingdatapro.com`
- **OpenAPI Spec:** `https://api.tradingdatapro.com/openapi-spec.json`
- **MCP Spec:** `https://api.tradingdatapro.com/.well-known/mcp.json`
- **Free Tier:** `https://api.tradingdatapro.com/api/signals/free`

## Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/YOUR_GITHUB_USER/antiretail-langchain-tool.git
    cd antiretail-langchain-tool
    ```
2.  Install dependencies:
    ```bash
    pip install langchain langchain-community python-dotenv requests
    ```

## Usage

1.  **Get an API Key:**
    The Anti-Retail Crypto Data API requires an API key for full access. Visit [https://api.tradingdatapro.com](https://api.tradingdatapro.com) to subscribe and get your key.

2.  **Set up Environment Variables:**
    Create a `.env` file in the root of this project with your API key:
    ```
    ANTI_RETAIL_API_KEY="your_api_key_here"
    ```

3.  **Run the Example Agent:**
    (See `antiretail_tool.py` for implementation details and `example_agent.py` for a basic agent using the tool.)
    ```bash
    python example_agent.py
    ```

## Example `antiretail_tool.py` (Custom LangChain Tool)

```python
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
```

## Example `example_agent.py` (Basic LangChain Agent)

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI # Using OpenAI for agent logic, replace as needed
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from antiretail_tool import get_anti_retail_signals # Import the custom tool

load_dotenv()

# --- Configure your LLM (e.g., OpenAI, Anthropic, Gemini) ---
# For OpenAI
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
# llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)

# For Anthropic Claude (ensure ANTHROPIC_API_KEY is set in .env)
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-opus-20240229", temperature=0)

# For Google Gemini (ensure GOOGLE_API_KEY is set in .env)
# from langchain_google_genai import ChatGoogleGenerativeAI
# llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# --- Define the tools the agent can use ---
# The custom tool from antiretail_tool.py
tools = [
    get_anti_retail_signals,
]

# --- Create the agent prompt ---
# This is a basic prompt; for complex agents, you'd refine this.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert crypto market analyst. Use the available tools to provide insights into market conditions."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# --- Create the agent ---
agent = create_tool_calling_agent(llm, tools, prompt)

# --- Create the agent executor ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Run the agent ---
if __name__ == "__main__":
    print("\n--- Running Anti-Retail Agent ---")
    response = agent_executor.invoke({"input": "What are the current anti-retail signals for Bitcoin?"})
    print(f"\nAgent Response: {response['output']}")

    print("\n--- Running Anti-Retail Agent (general market overview) ---")
    response = agent_executor.invoke({"input": "Give me a general crypto market overview with anti-retail insights."})
    print(f"\nAgent Response: {response['output']}")

    print("\n--- Running Anti-Retail Agent (Ethereum signals) ---")
    response = agent_executor.invoke({"input": "Tell me about Ethereum's anti-retail signals."})
    print(f"\nAgent Response: {response['output']}")
```

## License

MIT License
