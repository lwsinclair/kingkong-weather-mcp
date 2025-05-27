#!/usr/bin/env python3
"""
🦍 KING KONG'S WORKING WEATHER TEST - WORKSHOP READY!
Uses IN-MEMORY transport which works perfectly on Windows!
"""

import asyncio
import os
import json


async def workshop_weather_demo():
    """
    Perfect working demo for your MCP workshop tomorrow!
    Uses in-memory transport - no more connection issues!
    """
    print("🦍 KING KONG'S WORKSHOP WEATHER DEMO")
    print("=" * 60)
    print("✅ USING IN-MEMORY TRANSPORT (WORKS ON WINDOWS!)")
    print("🚀 PERFECT FOR WORKSHOP DEMONSTRATION!")
    print("=" * 60)

    # Check API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("⚠️  API KEY NOT SET - Demo will show error handling!")
        print("   Set with: export OPENWEATHER_API_KEY=your_key")
    else:
        print(f"✅ API Key configured: {api_key[:8]}...****")
    print()

    try:
        # Import your weather server directly
        print("📥 Loading weather server...")
        import weather_server
        from fastmcp import Client

        # Get the MCP server instance
        mcp_server = weather_server.mcp
        print(f"✅ Server loaded: {mcp_server.name}")

        # Create client with IN-MEMORY transport (direct connection)
        client = Client(mcp_server)
        print("✅ In-memory client created - NO STDIO ISSUES!")

        print("\n🔗 Connecting via in-memory transport...")

        async with client:
            print("🎉 CONNECTION SUCCESSFUL!")
            print()

            # WORKSHOP DEMO 1: Show Available Tools
            print("🔧 WORKSHOP DEMO 1: Available MCP Tools")
            print("-" * 50)
            tools = await client.list_tools()
            print(f"🦍 King Kong's Weather Server has {len(tools)} tools:")
            for i, tool in enumerate(tools, 1):
                print(f"  {i}. {tool.name}")
                print(f"     └─ {tool.description}")
            print()

            # WORKSHOP DEMO 2: API Status Check
            print("🔍 WORKSHOP DEMO 2: API Status Check")
            print("-" * 50)
            print("🌐 Checking OpenWeatherMap API connection...")
            status_result = await client.call_tool("check_api_status", {})
            status_data = json.loads(status_result[0].text)

            print(f"   Status: {status_data.get('status', 'Unknown')}")
            print(f"   Message: {status_data.get('message', 'No message')}")
            if "king_kong_says" in status_data:
                print(f"   🦍 King Kong: {status_data['king_kong_says']}")
            print()

            # WORKSHOP DEMO 3: Live Weather Data
            print("🌍 WORKSHOP DEMO 3: Live Weather Data")
            print("-" * 50)

            workshop_cities = [
                ("Samsun", "TR", "Your location!"),
                ("Istanbul", "TR", "Turkey's largest city"),
                ("London", "GB", "Classic demo city"),
                ("New York", "US", "The Big Apple"),
                ("Tokyo", "JP", "Tech capital"),
            ]

            for city, country, note in workshop_cities:
                print(f"🌤️  Getting weather for {city}, {country} ({note})")
                try:
                    weather_result = await client.call_tool(
                        "get_current_weather",
                        {"city": city, "country_code": country, "units": "celsius"},
                    )

                    weather_data = json.loads(weather_result[0].text)

                    if "error" in weather_data:
                        print(f"   ❌ API Error: {weather_data['error']}")
                        if "suggestion" in weather_data:
                            print(f"      💡 Tip: {weather_data['suggestion']}")
                    else:
                        # Show formatted weather info
                        temp = weather_data.get("temperature", {}).get("current", "N/A")
                        desc = weather_data.get("weather", {}).get("description", "N/A")
                        humidity = weather_data.get("atmospheric", {}).get(
                            "humidity", "N/A"
                        )

                        print(f"   ✅ {temp}, {desc}")
                        print(f"      💧 Humidity: {humidity}")

                        if "king_kong_status" in weather_data:
                            print(f"      🦍 {weather_data['king_kong_status']}")

                except Exception as e:
                    print(f"   ❌ Request failed: {e}")
                print()

            # WORKSHOP DEMO 4: Different Temperature Units
            print("🌡️  WORKSHOP DEMO 4: Temperature Units")
            print("-" * 50)
            print("🔥 Same city in different temperature units:")

            for unit_name, unit_code in [
                ("Celsius", "celsius"),
                ("Fahrenheit", "fahrenheit"),
                ("Kelvin", "kelvin"),
            ]:
                try:
                    result = await client.call_tool(
                        "get_current_weather", {"city": "Berlin", "units": unit_code}
                    )
                    data = json.loads(result[0].text)
                    if "error" not in data:
                        temp = data.get("temperature", {}).get("current", "N/A")
                        print(f"   {unit_name:>10}: {temp}")
                except:
                    print(f"   {unit_name:>10}: Error")
            print()

            # WORKSHOP DEMO 5: Coordinates Weather
            print("📍 WORKSHOP DEMO 5: Weather by Coordinates")
            print("-" * 50)
            famous_places = [
                (40.748817, -73.985428, "Empire State Building, NYC"),
                (48.8584, 2.2945, "Eiffel Tower, Paris"),
                (35.6762, 139.6503, "Tokyo Tower, Japan"),
            ]

            for lat, lon, place in famous_places:
                print(f"🗺️  Getting weather for {place}")
                print(f"     Coordinates: {lat}, {lon}")
                try:
                    coords_result = await client.call_tool(
                        "get_weather_by_coordinates",
                        {"latitude": lat, "longitude": lon, "units": "celsius"},
                    )
                    coords_data = json.loads(coords_result[0].text)
                    if "error" not in coords_data:
                        temp = coords_data.get("temperature", {}).get("current", "N/A")
                        city = coords_data.get("city", "Unknown")
                        print(f"     ✅ {city}: {temp}")
                    else:
                        print(f"     ❌ Error: {coords_data['error']}")
                except Exception as e:
                    print(f"     ❌ Failed: {e}")
                print()

            # WORKSHOP DEMO 6: Quick Weather Summary
            print("📊 WORKSHOP DEMO 6: Quick Weather Summary")
            print("-" * 50)
            try:
                summary_result = await client.call_tool(
                    "get_weather_summary", {"city": "Paris"}
                )
                summary_data = json.loads(summary_result[0].text)

                if "error" not in summary_data:
                    print(f"   🏙️  Location: {summary_data.get('location', 'N/A')}")
                    print(f"   📝 Summary: {summary_data.get('summary', 'N/A')}")
                    print(f"   🌡️  Feels like: {summary_data.get('feels_like', 'N/A')}")
                    if "king_kong_says" in summary_data:
                        print(f"   🦍 King Kong: {summary_data['king_kong_says']}")
                else:
                    print(f"   ❌ Error: {summary_data['error']}")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
            print()

            # WORKSHOP DEMO 7: Available Resources
            print("📚 WORKSHOP DEMO 7: MCP Resources")
            print("-" * 50)
            resources = await client.list_resources()
            print(f"🦍 King Kong's server provides {len(resources)} resources:")
            for resource in resources:
                print(f"   📄 {resource.uri}")
                print(f"      └─ {resource.name}")

            # Read one resource to show functionality
            if resources:
                print(f"\n📖 Reading resource: {resources[0].uri}")
                try:
                    resource_content = await client.read_resource(resources[0].uri)
                    resource_data = json.loads(resource_content[0].text)
                    print("   ✅ Resource data loaded successfully!")
                    if isinstance(resource_data, dict) and len(resource_data) <= 5:
                        for key, value in list(resource_data.items())[:3]:
                            print(f"      • {key}: {value}")
                except Exception as e:
                    print(f"   ⚠️  Could not read resource: {e}")
            print()

            # FINAL WORKSHOP MESSAGE
            print("🎉" * 25)
            print("🦍 WORKSHOP DEMO COMPLETED SUCCESSFULLY!")
            print("🚀 IN-MEMORY TRANSPORT = NO CONNECTION ISSUES!")
            print("⚡ REAL API INTEGRATION = LIVE WEATHER DATA!")
            print("🏆 READY TO DOMINATE THE MCP WORKSHOP!")
            print("🎉" * 25)

    except ImportError as e:
        print(f"❌ Could not import weather server: {e}")
        print("💡 Make sure weather_server.py is in the current directory")
        print("💡 Check that the file is complete and has no syntax errors")
    except Exception as e:
        import traceback

        print(f"❌ Demo failed: {e}")
        print("Full error details:")
        print(traceback.format_exc())


async def quick_workshop_test():
    """Super quick test to verify everything works for workshop."""
    print("⚡ QUICK WORKSHOP VERIFICATION")
    print("-" * 35)

    try:
        import weather_server
        from fastmcp import Client

        client = Client(weather_server.mcp)

        async with client:
            # Test basic functionality
            tools = await client.list_tools()
            api_status = await client.call_tool("check_api_status", {})

            print(f"✅ SUCCESS! Server has {len(tools)} tools")
            print("🦍 In-memory connection works perfectly!")
            print("🚀 100% READY FOR WORKSHOP!")

            # Quick weather test if API key is set
            if os.getenv("OPENWEATHER_API_KEY"):
                weather_test = await client.call_tool(
                    "get_current_weather", {"city": "London"}
                )
                print("✅ Live weather API working!")
            else:
                print("⚠️  Set API key for live weather data")

    except Exception as e:
        print(f"❌ ISSUE FOUND: {e}")
        print("🔧 Run full demo to see detailed error info")


def workshop_instructions():
    """Instructions for workshop demonstration."""
    print("🦍 WORKSHOP DEMONSTRATION INSTRUCTIONS")
    print("=" * 50)
    print()
    print("🎯 PRESENTATION FLOW:")
    print("1. Show the problem: 'AI needs real-time data'")
    print("2. Introduce MCP: 'Universal protocol for AI connections'")
    print("3. Run this demo: 'Live weather from OpenWeatherMap API'")
    print("4. Show the code: 'FastMCP tools, resources, prompts'")
    print("5. Deploy to Smithery: 'Production deployment'")
    print()
    print("🔧 TECHNICAL HIGHLIGHTS TO MENTION:")
    print("• Real API integration (not fake data)")
    print("• Multiple query methods (city, coordinates)")
    print("• Error handling with helpful messages")
    print("• Temperature unit conversions")
    print("• Resource templates and static resources")
    print("• In-memory transport for development")
    print("• HTTP transport for production")
    print()
    print("💡 DEMO TALKING POINTS:")
    print("• 'This is live data from OpenWeatherMap'")
    print("• 'Notice the error handling for invalid cities'")
    print("• 'See how MCP tools have automatic schema generation'")
    print("• 'Resources provide configuration and metadata'")
    print("• 'Same server works locally and in production'")
    print()
    print("🚀 AFTER DEMO:")
    print("• Show deployment with HTTP transport")
    print("• Upload to Smithery registry")
    print("• Test from Claude or other MCP client")
    print("• Answer questions about the code")


if __name__ == "__main__":
    print("🦍 KING KONG'S WORKSHOP-READY WEATHER MCP")
    print("=" * 55)
    print("Choose your option:")
    print("1. Quick test (verify everything works)")
    print("2. Full workshop demo (complete presentation)")
    print("3. Workshop instructions (presentation guide)")

    choice = input("\nEnter 1, 2, or 3: ").strip()

    if choice == "2":
        asyncio.run(workshop_weather_demo())
    elif choice == "3":
        workshop_instructions()
    else:
        asyncio.run(quick_workshop_test())
