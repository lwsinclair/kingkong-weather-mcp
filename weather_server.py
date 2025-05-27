#!/usr/bin/env python3
"""
King Kong's REAL Weather MCP Server
Using OpenWeatherMap API for live weather data!
🦍 WORKSHOP READY! 🌤️
"""

from fastmcp import FastMCP, Context
import httpx
import os
from datetime import datetime
from typing import Dict, Optional
import asyncio

# Initialize the MCP server
mcp = FastMCP(
    name="KingKongWeatherMCP",
    instructions="""
    🦍 King Kong's Weather MCP Server - REAL WEATHER DATA! 
    Provides current weather information using OpenWeatherMap API.
    Features:
    - Current weather by city name
    - Current weather by coordinates  
    - Weather with detailed metrics
    - Multiple temperature units (Celsius, Fahrenheit, Kelvin)
    """,
)

# OpenWeatherMap configuration
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Set this environment variable!

# HTTP client for API calls
http_client = httpx.AsyncClient(timeout=10.0)

# ============== HELPER FUNCTIONS ==============


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return round(kelvin - 273.15, 1)


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit."""
    return round((kelvin - 273.15) * 9 / 5 + 32, 1)


def format_weather_response(data: dict, units: str = "celsius") -> Dict:
    """Format OpenWeatherMap response into clean structure."""
    try:
        # Temperature conversions
        temp_k = data["main"]["temp"]
        feels_like_k = data["main"]["feels_like"]

        if units.lower() == "fahrenheit":
            temp = kelvin_to_fahrenheit(temp_k)
            feels_like = kelvin_to_fahrenheit(feels_like_k)
            temp_unit = "°F"
        elif units.lower() == "kelvin":
            temp = round(temp_k, 1)
            feels_like = round(feels_like_k, 1)
            temp_unit = "K"
        else:  # Default to Celsius
            temp = kelvin_to_celsius(temp_k)
            feels_like = kelvin_to_celsius(feels_like_k)
            temp_unit = "°C"

        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "coordinates": {
                "latitude": data["coord"]["lat"],
                "longitude": data["coord"]["lon"],
            },
            "weather": {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
            },
            "temperature": {
                "current": f"{temp}{temp_unit}",
                "feels_like": f"{feels_like}{temp_unit}",
                "min": f"{kelvin_to_celsius(data['main']['temp_min']) if units == 'celsius' else kelvin_to_fahrenheit(data['main']['temp_min']) if units == 'fahrenheit' else data['main']['temp_min']}{temp_unit}",
                "max": f"{kelvin_to_celsius(data['main']['temp_max']) if units == 'celsius' else kelvin_to_fahrenheit(data['main']['temp_max']) if units == 'fahrenheit' else data['main']['temp_max']}{temp_unit}",
            },
            "atmospheric": {
                "pressure": f"{data['main']['pressure']} hPa",
                "humidity": f"{data['main']['humidity']}%",
                "visibility": (
                    f"{data.get('visibility', 'N/A')} meters"
                    if data.get("visibility")
                    else "N/A"
                ),
            },
            "wind": {
                "speed": f"{data.get('wind', {}).get('speed', 0)} m/s",
                "direction": (
                    f"{data.get('wind', {}).get('deg', 'N/A')}°"
                    if data.get("wind", {}).get("deg")
                    else "N/A"
                ),
            },
            "clouds": f"{data.get('clouds', {}).get('all', 0)}%",
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime(
                "%H:%M:%S"
            ),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime(
                "%H:%M:%S"
            ),
            "timezone": f"UTC{data['timezone']//3600:+d}",
            "data_timestamp": datetime.fromtimestamp(data["dt"]).isoformat(),
            "king_kong_status": "🦍 LIVE WEATHER DATA DELIVERED!",
        }
    except KeyError as e:
        return {"error": f"Failed to parse weather data: missing field {e}"}


# ============== TOOLS ==============


@mcp.tool()
async def get_current_weather(
    city: str,
    country_code: Optional[str] = None,
    units: str = "celsius",
    ctx: Context = None,
) -> Dict:
    """
    Get current weather for a city using OpenWeatherMap API.

    Args:
        city: City name (e.g., "London", "New York")
        country_code: Optional 2-letter country code (e.g., "US", "GB")
        units: Temperature units - "celsius", "fahrenheit", or "kelvin"
    """
    if not API_KEY:
        return {
            "error": "🦍 KING KONG NEEDS API KEY! Set OPENWEATHER_API_KEY environment variable",
            "help": "Get free API key from: https://openweathermap.org/api",
        }

    if ctx:
        await ctx.info(f"🦍 King Kong fetching weather for {city}...")

    try:
        # Build query string
        query = city
        if country_code:
            query = f"{city},{country_code}"

        # Make API request
        url = f"{OPENWEATHER_BASE_URL}/weather"
        params = {"q": query, "appid": API_KEY}

        response = await http_client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if ctx:
                await ctx.info(
                    f"✅ Weather data retrieved for {data['name']}, {data['sys']['country']}"
                )
            return format_weather_response(data, units)
        elif response.status_code == 404:
            return {
                "error": f"City '{city}' not found",
                "suggestion": "Check spelling or try with country code (e.g., 'Paris,FR')",
            }
        elif response.status_code == 401:
            return {
                "error": "Invalid API key",
                "help": "Check your OPENWEATHER_API_KEY environment variable",
            }
        else:
            return {
                "error": f"API request failed with status {response.status_code}",
                "details": response.text,
            }

    except httpx.RequestError as e:
        return {
            "error": "Network error occurred",
            "details": str(e),
            "suggestion": "Check your internet connection",
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "king_kong_says": "🦍 Something went wrong, but King Kong will fix it!",
        }


@mcp.tool()
async def get_weather_by_coordinates(
    latitude: float, longitude: float, units: str = "celsius", ctx: Context = None
) -> Dict:
    """
    Get current weather by geographical coordinates.

    Args:
        latitude: Latitude coordinate (-90 to 90)
        longitude: Longitude coordinate (-180 to 180)
        units: Temperature units - "celsius", "fahrenheit", or "kelvin"
    """
    if not API_KEY:
        return {
            "error": "🦍 KING KONG NEEDS API KEY! Set OPENWEATHER_API_KEY environment variable"
        }

    # Validate coordinates
    if not (-90 <= latitude <= 90):
        return {"error": "Latitude must be between -90 and 90"}
    if not (-180 <= longitude <= 180):
        return {"error": "Longitude must be between -180 and 180"}

    if ctx:
        await ctx.info(
            f"🦍 King Kong fetching weather for coordinates ({latitude}, {longitude})..."
        )

    try:
        url = f"{OPENWEATHER_BASE_URL}/weather"
        params = {"lat": latitude, "lon": longitude, "appid": API_KEY}

        response = await http_client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if ctx:
                await ctx.info(
                    f"✅ Weather data retrieved for {data.get('name', 'Unknown location')}"
                )
            return format_weather_response(data, units)
        else:
            return {
                "error": f"API request failed with status {response.status_code}",
                "details": response.text,
            }

    except Exception as e:
        return {"error": f"Error fetching weather: {str(e)}"}


@mcp.tool()
async def get_weather_summary(city: str, ctx: Context = None) -> Dict:
    """
    Get a concise weather summary perfect for quick updates.

    Args:
        city: City name to get weather for
    """
    if ctx:
        await ctx.info(f"🦍 Getting quick weather summary for {city}...")

    weather_data = await get_current_weather(city, units="celsius", ctx=ctx)

    if "error" in weather_data:
        return weather_data

    # Create concise summary
    return {
        "location": f"{weather_data['city']}, {weather_data['country']}",
        "summary": f"{weather_data['temperature']['current']} - {weather_data['weather']['description']}",
        "feels_like": weather_data["temperature"]["feels_like"],
        "humidity": weather_data["atmospheric"]["humidity"],
        "wind": weather_data["wind"]["speed"],
        "king_kong_says": f"🦍 {weather_data['weather']['description']} in {weather_data['city']}! Perfect weather for conquering the world!",
    }


@mcp.tool()
async def check_api_status(ctx: Context = None) -> Dict:
    """Check if OpenWeatherMap API is working and API key is valid."""
    if not API_KEY:
        return {
            "status": "❌ No API Key",
            "message": "Set OPENWEATHER_API_KEY environment variable",
            "get_key": "https://openweathermap.org/api",
        }

    if ctx:
        await ctx.info("🦍 King Kong checking API status...")

    try:
        # Test API with London
        url = f"{OPENWEATHER_BASE_URL}/weather"
        params = {"q": "London,GB", "appid": API_KEY}

        response = await http_client.get(url, params=params)

        if response.status_code == 200:
            return {
                "status": "✅ API Working",
                "message": "OpenWeatherMap API is ready!",
                "king_kong_says": "🦍 ALL SYSTEMS GO! Ready to fetch weather data!",
            }
        elif response.status_code == 401:
            return {
                "status": "❌ Invalid API Key",
                "message": "Check your OPENWEATHER_API_KEY",
            }
        else:
            return {
                "status": f"⚠️ API Error: {response.status_code}",
                "message": response.text,
            }

    except Exception as e:
        return {
            "status": "❌ Connection Error",
            "message": f"Could not connect to OpenWeatherMap: {str(e)}",
        }


# ============== RESOURCES ==============


@mcp.resource("config://weather-api")
def get_api_config() -> Dict:
    """Get weather API configuration and status."""
    return {
        "api_provider": "OpenWeatherMap",
        "api_version": "2.5",
        "base_url": OPENWEATHER_BASE_URL,
        "api_key_configured": bool(API_KEY),
        "supported_units": ["celsius", "fahrenheit", "kelvin"],
        "supported_queries": ["city_name", "city_name,country_code", "coordinates"],
        "king_kong_power": "🦍 UNLIMITED WEATHER POWER!",
    }


@mcp.resource("data://supported-cities")
def get_popular_cities() -> Dict:
    """Get list of popular cities for testing."""
    return {
        "popular_cities": [
            "London,GB",
            "New York,US",
            "Tokyo,JP",
            "Paris,FR",
            "Sydney,AU",
            "Berlin,DE",
            "Mumbai,IN",
            "São Paulo,BR",
            "Cairo,EG",
            "Moscow,RU",
            "Beijing,CN",
            "Los Angeles,US",
        ],
        "usage_examples": [
            "get_current_weather('London')",
            "get_current_weather('New York', 'US')",
            "get_weather_by_coordinates(51.5074, -0.1278)",  # London coordinates
        ],
        "king_kong_favorites": ["New York,US", "Tokyo,JP", "King Kong Island"],
    }


# ============== PROMPTS ==============


@mcp.prompt()
def weather_report_prompt(city: str, detailed: bool = False) -> str:
    """Generate a prompt for detailed weather reporting."""
    base_prompt = f"Please provide a weather report for {city}. Include current conditions, temperature, and any weather advisories."

    if detailed:
        base_prompt += " Provide detailed information including atmospheric pressure, humidity, wind conditions, and sunrise/sunset times."

    base_prompt += " Make the report engaging and informative for the user."

    return base_prompt


@mcp.prompt()
def travel_weather_prompt(cities: list, travel_date: str = "today") -> str:
    """Generate a prompt for travel weather planning."""
    cities_str = ", ".join(cities)
    return f"I'm planning to travel to {cities_str} {travel_date}. Please help me understand the weather conditions in these cities and provide recommendations for what to pack and any weather-related travel considerations."


# ============== CLEANUP ==============


async def cleanup():
    """Clean up HTTP client on shutdown."""
    await http_client.aclose()


# ============== HEALTH CHECK FOR DOCKER ==============


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health check endpoint for Docker/Smithery deployment."""
    from starlette.responses import JSONResponse

    # Quick API check
    api_working = bool(API_KEY)

    return JSONResponse(
        {
            "status": "healthy" if api_working else "degraded",
            "service": "KingKongWeatherMCP",
            "version": "1.0.0",
            "api_key_configured": api_working,
            "timestamp": datetime.now().isoformat(),
            "king_kong_says": "🦍 READY TO SERVE WEATHER DATA!",
        }
    )


# ============== MAIN ==============


def parse_args():
    """Parse command line arguments."""
    import argparse

    parser = argparse.ArgumentParser(description="King Kong's Weather MCP Server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "streamable-http", "sse"],
        help="Transport protocol",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    return parser.parse_args()


if __name__ == "__main__":
    # Reduced startup messages for STDIO deployment
    startup_msg = os.getenv("SHOW_STARTUP", "true").lower() == "true"

    if startup_msg:
        print("🦍 KING KONG'S WEATHER MCP SERVER STARTING...")
        print("🌤️ OpenWeatherMap API Integration Ready")
        if not API_KEY:
            print("⚠️  Set OPENWEATHER_API_KEY environment variable")

    try:
        # Register cleanup
        import atexit

        atexit.register(lambda: asyncio.run(cleanup()))

        # Check if running in deployment environment
        if os.getenv("SMITHERY_DEPLOYMENT") == "true":
            # For Smithery deployment - always use STDIO
            mcp.run(transport="stdio")
        else:
            # Parse command line arguments for local development
            args = parse_args()

            # Run the server with specified transport
            if args.transport == "streamable-http":
                if startup_msg:
                    print(f"🌐 HTTP server: http://{args.host}:{args.port}")
                mcp.run(transport="streamable-http", host=args.host, port=args.port)
            elif args.transport == "sse":
                if startup_msg:
                    print(f"📡 SSE server: http://{args.host}:{args.port}")
                mcp.run(transport="sse", host=args.host, port=args.port)
            else:
                if startup_msg:
                    print("📟 STDIO server ready")
                mcp.run(transport="stdio")

    except KeyboardInterrupt:
        if startup_msg:
            print("\n🦍 King Kong shutting down...")
        asyncio.run(cleanup())
    except Exception as e:
        if startup_msg:
            print(f"❌ Server error: {e}")
        asyncio.run(cleanup())
        raise
