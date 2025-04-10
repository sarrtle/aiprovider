"""Test."""

# inside tool choice array
from enum import Enum
from chat.tool import Tool
import json

tool1 = {
    "type": "function",
    "function": {
        "name": "Name of the function",
        "description": "Detailed info what the functio do.",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "description": "Param1 description",
                    "type": "string",
                },
                "param2": {
                    "description": "Param2 description",
                    "type": "number",
                },
            },
            "required": ["param1", "param2"],
        },
    },
}


class Unit(Enum):
    """Unit."""

    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


def get_weather(city: str, unit: Unit) -> str:
    """Get the weather of a city.

    Use Api to get the weather of chosen place.

    Args:
        city: The city to get the weather of.
        unit: The unit to return the weather in.

    Returns:
        The weather of the city.

    """
    return f"The weather in {city} is 20 degrees {unit}."


tool = Tool(get_weather)
json_schema = tool.generate_function_schema()

print(json.dumps(json_schema, indent=4))
