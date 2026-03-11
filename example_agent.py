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
