"""Tool object."""

import asyncio
from enum import Enum
import inspect
import re
from typing import Callable, Literal, cast, get_args, get_origin, get_type_hints


class Tool:
    """Tool."""

    def __init__(self, func: Callable[..., object]):
        """Initialize Tool."""
        self._function: Callable[..., object] = func
        self._args: dict[str, object] = {}
        self._function_response: object = object
        self._tool_id: str = ""
        self.name: str = self._function.__name__

    def register(self, args_dict: dict[str, object], tool_id: str):
        """Store the arguments and tool id."""
        self._args = args_dict
        self._tool_id = tool_id
        return self

    async def run(self):
        """Run function."""
        if not self._args:
            raise ValueError("No arguments provided.")

        if inspect.iscoroutinefunction(self._function):
            self._function_response = cast(object, await self._function(**self._args))

        # run synchronous function in thread pool
        loop = asyncio.get_running_loop()
        self._function_response = await loop.run_in_executor(
            None, self._function, *self._args.values()
        )

    @property
    def tool_id(self) -> str:
        """Tool id."""
        if not self._tool_id:
            raise ValueError("Tool id not set.")
        return self._tool_id

    @property
    def function_response(self) -> object:
        """Function response."""
        return self._function_response

    def generate_function_schema(self) -> dict[str, object]:
        """Generate a json schema for function calling.

        Returns:
            json schema

        Examples:
            ```json
            {
                 "name": "get_weather",
                 "description": "Get the weather of a city.",
                 "parameters": {
                     "type": "object",
                     "properties": {
                         "city": {
                             "description": "The city to get the weather of.",
                             "type": "string",
                         },
                         "unit": {
                             "description": "The unit to return the weather in.",
                             "type": "string",
                         },
                     },
                     "required": ["city", "unit"],
                 },
            }
            ```

        """
        function_name = self._function.__name__
        function_docstring = self._function.__doc__ or ""
        params_dict: dict[str, dict[str, str | list[str | int]]] = {}

        if not self._function.__doc__:
            raise ValueError("Function must have a docstring.")

        # extract information from docstring
        lines = [line.strip() for line in function_docstring.split("\n")]

        # get function description, first sentence of Google
        # styled docstring
        function_description = re.split(r"\.\s|\.\n", lines[0])[0].strip()

        # parse params from docstring
        in_args = False
        for line in lines:
            if line.lower().startswith("args:"):
                in_args = True
                continue
            if in_args and ":" in line:
                param, desc = line.split(":", 1)
                params_dict[param.strip()] = {"description": desc.strip()}

            # end of args section
            elif in_args and not line:
                break

        # get param types from the function signature
        # using inspect module
        function_signature = inspect.signature(self._function)

        type_hints = get_type_hints(self._function)
        for name, _param in function_signature.parameters.items():
            # skip self parameter
            if name == "self":
                continue

            # get parameter type
            raw_type = type_hints.get(name, None)

            # check for literal types
            origin = get_origin(raw_type)
            if origin is Literal:
                literal_values = cast(tuple[str | int], get_args(raw_type))
                # determine the json type base on literal values
                if literal_values and all(
                    isinstance(val, str) for val in literal_values
                ):
                    json_type = "string"
                elif literal_values and all(
                    isinstance(val, int) for val in literal_values
                ):
                    json_type = "number"
                else:
                    raise ValueError(f"Literal type {raw_type} is not supported.")

                params_dict[name]["type"] = json_type
                params_dict[name]["enum"] = list(literal_values)

            # check for real enum types
            elif isinstance(raw_type, type) and issubclass(raw_type, Enum):
                enum_values = cast(
                    list[str | int], [member.value for member in raw_type]
                )

                if enum_values and all(isinstance(val, str) for val in enum_values):
                    json_type = "string"
                elif enum_values and all(isinstance(val, int) for val in enum_values):
                    json_type = "number"
                else:
                    raise ValueError(f"Enum type {raw_type} is not supported.")

                params_dict[name]["type"] = json_type
                params_dict[name]["enum"] = enum_values

            # map common python types to json schema
            elif raw_type is str:
                json_type = "string"
            elif raw_type is int:
                json_type = "number"
            elif raw_type is float:
                json_type = "number"
            elif raw_type is bool:
                json_type = "boolean"
            elif origin is list:
                json_type = "array"
            elif raw_type is dict:
                json_type = "object"
            else:
                raise ValueError(f"Type {raw_type} is not supported.")

            # add param to params dict
            if name not in params_dict:
                params_dict[name] = {}

            params_dict[name]["type"] = json_type

        # Determine required parameters (those without a default value)
        # Note: param.default is always `inspect.Parameter.empty`
        #       developers just forgot to put types that is why it is an `Any`
        required_fields = [
            name
            for name, param in function_signature.parameters.items()
            if name != "self" and cast(object, param.default) is inspect.Parameter.empty
        ]

        return {
            "name": function_name,
            "description": function_description,
            "parameters": {
                "type": "object",
                "properties": params_dict,
                "required": required_fields,
            },
        }
