# ft_raise_errors.py

def check_plant_health(plant_name, water_level, sunlight_hours):
    # Check plant name
    if not plant_name or plant_name.strip() == "":
        raise ValueError("Plant name cannot be empty!")

    # Check water level
    if water_level < 1:
        raise ValueError(f"Water level {water_level} is too low (min 1)")
    if water_level > 10:
        raise ValueError(f"Water level {water_level} is too high (max 10)")

    # Check sunlight hours
    if sunlight_hours < 2:
        raise ValueError(f"Sunlight hours {sunlight_hours} is too low (min 2)")
    if sunlight_hours > 12:
        raise ValueError(f"Sunlight hours {sunlight_hours} is too high (max 12)")

    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks():
    print("=== Garden Plant Health Checker ===")

    # Test 1: good values
    try:
        print("Testing good values...")
        result = check_plant_health("tomato", 5, 6)
        print(result)
    except ValueError as e:
        print("Error:", e)

    # Test 2: bad plant name
    try:
        print("Testing empty plant name...")
        result = check_plant_health("", 5, 6)
        print(result)
    except ValueError as e:
        print("Error:", e)

    # Test 3: bad water level
    try:
        print("Testing bad water level...")
        result = check_plant_health("carrot", 15, 6)
        print(result)
    except ValueError as e:
        print("Error:", e)

    # Test 4: bad sunlight hours
    try:
        print("Testing bad sunlight hours...")
        result = check_plant_health("lettuce", 5, 0)
        print(result)
    except ValueError as e:
        print("Error:", e)

    print("All error raising tests completed!")


# Run tests
if __name__ == "__main__":
    test_plant_checks()
