import os
import requests
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import re
from langchain.prompts import ChatPromptTemplate

# Load environment variables from .env
load_dotenv()

# Get the Weather API key from environment variables
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")


@tool
def get_weather(location: str) -> str:
    """Fetch the current weather for a given location using WeatherAPI."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error getting weather for {location}: {response.text}"
    
    data = response.json()
    weather_description = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    feels_like = data["current"]["feelslike_c"]
    humidity = data["current"]["humidity"]
    wind_speed = data["current"]["wind_kph"]
    
    return (
        f"Current weather in {location}: {weather_description}. "
        f"Temperature: {temperature}°C (feels like {feels_like}°C). "
        f"Humidity: {humidity}%. Wind speed: {wind_speed} km/h."
    )


@tool
def recommend_clothing(weather_info: str) -> str:
    """Recommend clothing based on parsed weather information."""
    # Extract temperature from the weather string
    temp_match = re.search(r'Temperature: ([\d.]+)°C', weather_info)
    if not temp_match:
        return "Could not determine temperature from weather information."
    
    temperature = float(temp_match.group(1))
    weather_description = weather_info.lower()
    
    # Define temperature categories
    cold = temperature < 10
    cool = 10 <= temperature < 18
    mild = 18 <= temperature < 24
    warm = 24 <= temperature < 30
    hot = temperature >= 30
    
    # Detect special conditions
    rainy = any(x in weather_description for x in ["rain", "drizzle", "shower"])
    snowy = any(x in weather_description for x in ["snow", "sleet", "hail"])
    windy = "wind" in weather_description
    sunny = any(x in weather_description for x in ["sun", "clear", "sunny"])
    
    # Start building clothing recommendations
    recommendations = []
    
    # Add temperature-based clothing
    if cold:
        recommendations.extend([
            "Heavy coat or down jacket",
            "Thermal underwear",
            "Sweater or fleece",
            "Warm hat",
            "Gloves",
            "Scarf",
            "Thick socks",
            "Boots"
        ])
    elif cool:
        recommendations.extend([
            "Light jacket or coat",
            "Sweater or light fleece",
            "Long-sleeve shirt",
            "Jeans or pants",
            "Light scarf (optional)",
            "Closed shoes"
        ])
    elif mild:
        recommendations.extend([
            "Light sweater or cardigan",
            "Long or short-sleeve shirt",
            "Pants or jeans",
            "Sneakers or casual shoes"
        ])
    elif warm:
        recommendations.extend([
            "T-shirt or short-sleeve shirt",
            "Light pants or shorts",
            "Dress or skirt",
            "Sandals or sneakers",
            "Light hat for sun protection"
        ])
    elif hot:
        recommendations.extend([
            "Lightweight t-shirt or tank top",
            "Shorts or light skirt",
            "Sandals",
            "Sunglasses",
            "Sun hat",
            "Breathable fabrics (cotton, linen)"
        ])
    
    # Adjust for special conditions
    if rainy:
        recommendations.extend([
            "Raincoat or waterproof jacket",
            "Umbrella",
            "Waterproof shoes or boots"
        ])
    if snowy:
        recommendations.extend([
            "Waterproof boots with good traction",
            "Waterproof jacket and pants",
            "Insulated gloves"
        ])
    if windy:
        recommendations.append("Windbreaker or jacket that blocks wind")
    if sunny:
        recommendations.extend([
            "Sunglasses",
            "Sunscreen",
            "Hat for sun protection"
        ])
    
    return "Recommended clothing:\n- " + "\n- ".join(set(recommendations))  # Remove duplicates


# Prompt template for the ReAct agent
prompt = ChatPromptTemplate.from_template(
    """You are a clothing recommendation assistant. Based on current weather information, you help users decide what to wear.
Always respond **only in English**, in a warm and user-friendly tone.

Your response should:
- Include a short weather summary (e.g. "The weather is sunny in Istanbul and 24°C.")
- Suggest appropriate clothing items clearly
- Be written as a full, natural sentence, not a list

Available tools:
{tools}

Use this format:

Question: the user's question
Thought: think about what you need to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation cycle can repeat N times)
Thought: I now know the final answer
Final Answer: your final answer to the original question (must be in English and user-friendly)

Begin!

Question: {input}
{agent_scratchpad}"""
)

# Initialize ChatOpenAI model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define available tools for the agent
tools = [get_weather, recommend_clothing]

# Create the ReAct agent with tools and prompt
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Create an executor that runs the agent with the defined tools
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
