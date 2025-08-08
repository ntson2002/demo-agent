def cprint(*args, color="default", **kwargs):
    print_text_with_color(*args, color=color, **kwargs)


def print_text_with_color(*args, color="default", **kwargs):
    colors = {
        "default": "\033[0m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "purple": "\033[95m",
    }

    try:
        color_code = colors.get(color.lower(), colors["default"])
        print(f"{color_code}", end="")  # Start color
        print(*args, **kwargs)
        print("\033[0m", end="")  # Reset color
    except:
        pass


def function_to_json(func) -> dict:
    import inspect
    """
    Sample Input:
    def add_two_numbers(a: int, b: int) -> int:
        # Adds two numbers together
        return a + b
    
    Sample Output:
    {
        'type': 'function',
        'function': {
            'name': 'add_two_numbers',
            'description': 'Adds two numbers together',
            'parameters': {
                'type': 'object',
                'properties': {
                    'a': {'type': 'integer'},
                    'b': {'type': 'integer'}
                },
                'required': ['a', 'b']
            }
        }
    }
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }