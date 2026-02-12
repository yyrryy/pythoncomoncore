class GardenError(Exception):
    def __init__(self, message="Garden error occurred"):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message="Plant problem occurred"):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message="Watering problem happened"):
        super().__init__(message)


def check_space(space_available):
    if space_available < 10:
        raise GardenError("Not enough space in the garden!")


def check_status(status):
    if status == "wilting":
        raise PlantError("The tomato plant is wilting!")


def check_water(water_level):
    if water_level <= 5:
        raise WaterError("Not enough water in the tank!")


def test_custom_errors():
    print("=== Custom Garden Errors Demo ===")
    try:
        print("Testing GardenError...")
        check_space(5)
    except GardenError as e:
        print(f"Caught GardenError: {e}\n")
    try:
        print("Testing PlantError...")
        check_status("wilting")
    except PlantError as e:
        print(f"Caught PlantError: {e}\n")
 
    # Test WaterError
    try:
        print("Testing WaterError...")
        check_water(4)
    except WaterError as e:
        print(f"Caught WaterError: {e}\n")

    # Catch all garden errors (parent class)
    print("Testing catching all garden errors...")

    try:
        check_water(0)
    except GardenError as e:
        print("Caught a garden error:", e)
    try:
        check_status("wilting")
    except GardenError as e:
        print("Caught a garden error:", e)

    print("All custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
