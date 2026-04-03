from typing import Optional
from datetime import datetime
import sys

try:
    from pydantic import BaseModel, Field, ValidationError
except ModuleNotFoundError:
    print("Pydantic is not installed, pip install it")
    sys.exit(1)


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main():
    print("Space Station Data Validation")
    print("=" * 40)
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-03-20T14:30:00",
            notes="Primary orbital research station"
        )

        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(f"Status: {'Operational' if station.is_operational else 'Non-operational'}")

    except ValidationError as e:
        print("Validation error (unexpected):")
        print(e)

    print("=" * 40)
    print("Testing invalid data")
    try:
        o = SpaceStation(
            station_id="BAD001",
            name="Faulty Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now()
        )
    o.name = True
    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err['msg'])


if __name__ == "__main__":
    main()
