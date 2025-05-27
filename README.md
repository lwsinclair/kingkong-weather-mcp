# 🦍 King Kong's Weather MCP Server

A professional Model Context Protocol (MCP) server providing real-time weather data through OpenWeatherMap API integration.

## Features

🌤️ **Live Weather Data** - Real-time weather from OpenWeatherMap API  
🌍 **Multiple Query Methods** - Search by city name, coordinates, or country codes  
🌡️ **Temperature Units** - Support for Celsius, Fahrenheit, and Kelvin  
🛡️ **Error Handling** - Graceful error handling with helpful messages  
📊 **Rich Data** - Temperature, humidity, wind, atmospheric pressure, and more  
🔧 **MCP Standard** - Full MCP protocol compliance with tools and resources  

## Quick Start

### 1. Get API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard

### 2. Configuration
When deploying on Smithery, you'll be prompted to enter:
- **API Key**: Your OpenWeatherMap API key (required)
- **Default Units**: Temperature units (celsius/fahrenheit/kelvin)
- **Timeout**: API request timeout in seconds

### 3. Available Tools

#### `get_current_weather`
Get current weather for any city
```json
{
  "city": "London",
  "country_code": "GB",
  "units": "celsius"
}
```

#### `get_weather_by_coordinates`
Get weather by geographical coordinates
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "units": "fahrenheit"
}
```

#### `get_weather_summary`
Get concise weather summary
```json
{
  "city": "Tokyo"
}
```

#### `check_api_status`
Verify API connectivity and configuration
```json
{}
```

### 4. Resources

- `config://weather-api` - API configuration and capabilities
- `data://supported-cities` - List of popular cities for testing

## Example Usage

```javascript
// Get London weather
await callTool("get_current_weather", {
  city: "London",
  country_code: "GB",
  units: "celsius"
});

// Get weather by coordinates (NYC)
await callTool("get_weather_by_coordinates", {
  latitude: 40.7128,
  longitude: -74.0060,
  units: "fahrenheit"
});
```

## Built With

- **FastMCP** - MCP server framework
- **OpenWeatherMap API** - Weather data provider
- **Python 3.11** - Runtime environment

## Workshop Project

This server was built as part of an MCP workshop demonstration, showcasing:
- Real API integration patterns
- Professional error handling
- MCP protocol best practices
- Production deployment techniques

---

**🦍 Built by King Kong for the MCP community!**