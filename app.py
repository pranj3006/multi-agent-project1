import os
import certifi
import requests

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

search_tool = TavilySearchResults(api_key=TAVILY_API_KEY,max_results=3)
@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather data for a city from weatherstak.com"""    
    if not WEATHERSTACK_API_KEY:
        raise ValueError("WEATHERSTACK_API_KEY is not set in the environment variables.")

    url = f"http://api.weatherstack.com/current?access_key={WEATHERSTACK_API_KEY}&query={city}"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        return f"Error fetching weather data: {data['error']['info']}"

    if "current" not in data:
        return "Error: No current weather data found."
    current_weather = data.get("current", {})
    temperature = current_weather.get("temperature")
    humidity = current_weather.get("humidity")
    weather_descriptions = current_weather.get("weather_descriptions", [])
    description = weather_descriptions[0] if weather_descriptions else "No description available"

    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "description": description
    }
def create_agent_executor():
    """Create the configured agent executor for interactive use."""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is not set in the environment variables.")

    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
    )
    prompt = hub.pull("hwchase17/react")
    tools = [search_tool]
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
