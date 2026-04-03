from typing import Any, Dict, Tuple, Set


class InvalideValue(Exception):
    """Custom exception raised for invalid configuration values."""
    pass


def parsing_line(line: str) -> Tuple[str, Any]:
    """
    Parses a single line from the config file into a key and a typed value.

    Args:
        line: A string representing one line from the config file.

    Returns:
        A tuple containing the key (str) and the parsed value (Any).

    Raises:
        ValueError: If the line format is incorrect or values are invalid.
        InvalideValue: If the key is unknown or file path is restricted.
    """
    line = line.strip()
    if "=" not in line:
        raise ValueError(f"Invalid line: {line}")

    key_raw, value_raw = line.split("=", 1)
    key: str = key_raw.upper().strip()
    value_str: str = value_raw.strip()

    final_value: Any

    if key in ("WIDTH", "HEIGHT"):
        if not value_str.isdigit():
            raise ValueError(
                f"{key} must be a positive integer. Got: {value_str}"
                )
        final_value = int(value_str)

    elif key in ("ENTRY", "EXIT"):
        parts = value_str.split(",")
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            raise ValueError(f"{key} must be in format x,y. Got: {value_str}")
        final_value = tuple(int(p.strip()) for p in parts)

    elif key == "PERFECT":
        low_value = value_str.lower()
        if low_value not in ("true", "false"):
            raise ValueError(
                f"PERFECT must be True or False. Got: {value_str}"
                )
        final_value = (low_value == "true")

    elif key == "SEED":
        if value_str == "":
            raise ValueError("invalid input seed can just be "
                  "(int, float, str, bytes, None)")
        final_value = value_str

    elif key == "OUTPUT_FILE":
        if not value_str:
            raise InvalideValue("OUTPUT_FILE cannot be empty")
        if value_str.endswith(".py"):
            raise InvalideValue(
                "OUTPUT_FILE cannot be a .py file for security"
                )
        final_value = value_str
        try:
            open(final_value, 'w')
        except Exception as e:
            raise InvalideValue(f"cant open: {e}")
    else:
        raise InvalideValue(f"Unknown key: {key}")

    return key, final_value


def validate_config(config: dict) -> None:
    """
    Validates the entire configuration dictionary against maze rules.

    Args:
        config: Dictionary containing all parsed settings.

    Raises:
        ValueError: If keys are missing or logic (bounds/size) is violated.
    """
    required_keys: Set[str] = {
        "WIDTH", "HEIGHT", "ENTRY",
        "EXIT", "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - config.keys()
    if missing:
        raise ValueError(f"Missing configuration keys: {missing}")

    if config["WIDTH"] <= 8:
        raise ValueError("WIDTH must be greater than 8")
    if config["HEIGHT"] <= 6:
        raise ValueError("HEIGHT must be greater than 6")
    x_entry, y_entry = config["ENTRY"]
    x_exit, y_exit = config["EXIT"]

    if not (0 <= x_entry < config["WIDTH"]
            and 0 <= y_entry < config["HEIGHT"]):
        raise ValueError("ENTRY is outside maze bounds")

    if not (0 <= x_exit < config["WIDTH"] and 0 <= y_exit < config["HEIGHT"]):
        raise ValueError("EXIT is outside maze bounds")

    if config["ENTRY"] == config["EXIT"]:
        raise ValueError("Entry point and Exit point cannot be the same")


def read_file(path: str = "config.txt") -> Dict[str, Any]:
    """
    Reads and parses the configuration file.

    Args:
        path: Path to the config file. Default is 'config.txt'.

    Returns:
        A validated configuration dictionary.
    """
    config: Dict[str, Any] = {}

    try:
        with open(path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = parsing_line(line)

                if key in config:
                    raise InvalideValue(
                        f"Duplicate key '{key}' found on line {line_number}"
                    )

                config[key] = value
    except FileNotFoundError:
        raise InvalideValue(
            f"The file '{path}' was not found"
            )
    except PermissionError:
        raise InvalideValue(
            f"The file '{path}' has no reading permissions"
            )
    validate_config(config)
    return config
