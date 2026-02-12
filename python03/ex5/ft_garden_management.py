# ft_garden_management.py

# ---------------- CUSTOM EXCEPTIONS ---------------- #

class GardenError(Exception):
    """Base class for garden-related errors."""
    pass


class PlantError(GardenError):
    """Raised when plant-related operations fail."""
    pass


class WaterTankError(GardenError):
    """Raised when watering system has problems (ex: empty tank)."""
    pass


class HealthCheckError(GardenError):
    """Raised when plant health check fails."""
    pass


# ---------------- GARDEN MANAGER CLASS ---------------- #

class GardenManager:
    def __init__(self):
        self.plants = {}  # plant_name -> {"water": int, "sun": int}
        self.water_tank = 10  # simulate limited water resource

    def add_plant(self, plant_name, water_level, sunlight_hours):
        if not plant_name or plant_name.strip() == "":
            raise PlantError("Plant name cannot be empty!")

        if plant_name in self.plants:
            raise PlantError(f"Plant '{plant_name}' already exists!")

        if water_level < 1 or water_level > 10:
            raise PlantError(f"Water level {water_level} must be between 1 and 10")

        if sunlight_hours < 2 or sunlight_hours > 12:
            raise PlantError(f"Sunlight hours {sunlight_hours} must be between 2 and 12")

        self.plants[plant_name] = {"water": water_level, "sun": sunlight_hours}

    def water_plant(self, plant_name, amount):
        if plant_name not in self.plants:
            raise PlantError(f"Plant '{plant_name}' not found!")

        if amount <= 0:
            raise WaterTankError("Water amount must be positive!")

        if self.water_tank < amount:
            raise WaterTankError("Not enough water in tank")

        self.plants[plant_name]["water"] += amount
        self.water_tank -= amount

    def check_plant_health(self, plant_name):
        if plant_name not in self.plants:
            raise HealthCheckError(f"Plant '{plant_name}' not found!")

        water_level = self.plants[plant_name]["water"]
        sunlight_hours = self.plants[plant_name]["sun"]

        if water_level < 1:
            raise HealthCheckError(f"Water level {water_level} is too low (min 1)")
        if water_level > 10:
            raise HealthCheckError(f"Water level {water_level} is too high (max 10)")

        if sunlight_hours < 2:
            raise HealthCheckError(f"Sunlight hours {sunlight_hours} is too low (min 2)")
        if sunlight_hours > 12:
            raise HealthCheckError(f"Sunlight hours {sunlight_hours} is too high (max 12)")

        return f"{plant_name}: healthy (water: {water_level}, sun: {sunlight_hours})"


# ---------------- TEST FUNCTION ---------------- #

def test_garden_management():
    print("=== Garden Management System ===")

    garden = GardenManager()

    print("Adding plants to garden...")
    try:
        garden.add_plant("tomato", 5, 8)
        print("Added tomato successfully")

        garden.add_plant("lettuce", 7, 6)
        print("Added lettuce successfully")

        garden.add_plant("", 5, 8)  # invalid name
        print("Added unnamed plant successfully")

    except PlantError as e:
        print("Error adding plant:", e)

    print("\nWatering plants...")
    print("Opening watering system")

    try:
        garden.water_plant("tomato", 2)
        print("Watering tomato - success")

        garden.water_plant("lettuce", 3)
        print("Watering lettuce - success")

    except (PlantError, WaterTankError) as e:
        print("Error watering plant:", e)

    finally:
        print("Closing watering system (cleanup)")

    print("\nChecking plant health...")

    # force an invalid value to demonstrate error handling
    garden.plants["lettuce"]["water"] = 15

    for plant in ["tomato", "lettuce"]:
        try:
            print(garden.check_plant_health(plant))
        except HealthCheckError as e:
            print(f"Error checking {plant}:", e)

    print("\nTesting error recovery...")
    try:
        garden.water_plant("tomato", 50)  # too much water needed
    except WaterTankError as e:
        print("Caught GardenError:", e)
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    test_garden_management()
