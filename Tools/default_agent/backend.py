from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
import requests

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

@tool
def get_conversion_rate(currency_from: str, currency_to: str):
    """Get current conversion rate from one currency to another"""
    try:
        url = f"https://open.er-api.com/v6/latest/{currency_from.upper()}"
        response = requests.get(url)
        data = response.json()
        
        if 'rates' in data and currency_to.upper() in data['rates']:
            return f"1 {currency_from.upper()} = {data['rates'][currency_to.upper()]} {currency_to.upper()}"
        else:
            return f"Currency {currency_to} not found"
    except Exception as e:
        return f"Error fetching conversion rate: {str(e)}"

@tool
def calc_conversion(currency_from: str, currency_to: str, amount: float):
    """Calculate currency conversion for a specific amount"""
    try:
        url = f"https://open.er-api.com/v6/latest/{currency_from.upper()}"
        response = requests.get(url)
        data = response.json()
        
        if 'rates' in data and currency_to.upper() in data['rates']:
            rate = data['rates'][currency_to.upper()]
            converted_amount = amount * rate
            return f"{amount} {currency_from.upper()} = {converted_amount:.2f} {currency_to.upper()}"
        else:
            return f"Currency {currency_to} not found"
    except Exception as e:
        return f"Error calculating conversion: {str(e)}"


tavily_tool = TavilySearch(max_results=3)

tools = [
    get_conversion_rate,
    calc_conversion,
    tavily_tool
]

memory = MemorySaver()
agent_executor = create_agent(
    llm,
    tools,
    checkpointer=memory
)

def invoke_llm(user_input: str, thread_id: str):
    system_msg = "Use web search ONLY for current/recent info, unknown facts, or explicit requests. DON'T use for general knowledge, programming, math, or definitions."
    response = agent_executor.invoke(
        {"messages": [("system", system_msg), ("user", user_input)]},
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )
    return response["messages"][-1].content