import os
import requests
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import re
from langchain.prompts import ChatPromptTemplate
load_dotenv()

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
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
    
    return f"Current weather in {location}: {weather_description}. Temperature: {temperature}°C (feels like {feels_like}°C). Humidity: {humidity}%. Wind speed: {wind_speed} km/h."


@tool
def recommend_clothing(weather_info: str) -> str:
    """Recommend clothing based on weather description. Input should be the output from get_weather."""
    # Parse temperature from the weather info string
    temp_match = re.search(r'Temperature: ([\d.]+)°C', weather_info)
    if not temp_match:
        return "Could not determine temperature from weather information."
    
    temperature = float(temp_match.group(1))
    weather_description = weather_info.lower()
    
    # Define temperature ranges
    cold = temperature < 10
    cool = 10 <= temperature < 18
    mild = 18 <= temperature < 24
    warm = 24 <= temperature < 30
    hot = temperature >= 30
    
    # Check weather conditions
    rainy = any(x in weather_description for x in ["rain", "drizzle", "shower"])
    snowy = any(x in weather_description for x in ["snow", "sleet", "hail"])
    windy = "wind" in weather_description
    sunny = any(x in weather_description for x in ["sun", "clear", "sunny"])
    
    # Base recommendations
    recommendations = []
    
    # Temperature-based recommendations
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
            "Consider light, breathable fabrics like cotton or linen"
        ])
    
    # Weather condition adjustments
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
    
    return "Recommended clothing:\n- " + "\n- ".join(set(recommendations))  # Using set to remove duplicates



prompt = ChatPromptTemplate.from_template(
    """You are a clothing recommendation assistant. Based on current weather information, you help users decide what to wear.
Always respond **only in Turkish**, in a warm and user-friendly tone.

Your response should:
- Include a short weather summary (e.g. "İstanbul’da hava güneşli ve 24°C.")
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
Final Answer: your final answer to the original question (must be in Turkish and user-friendly)

Begin!

Question: {input}
{agent_scratchpad}"""
)

# Set up ChatOpenAI model
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define the tools (functions)
tools = [get_weather, recommend_clothing]

# Initialize the agent with the prompt
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Set up the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

