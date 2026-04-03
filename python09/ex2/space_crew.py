from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import List
from enum import Enum
from datetime import datetime


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        if not any(member.rank in [Rank.commander, Rank.captain] for member in self.crew):
            raise ValueError("Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced = [m for m in self.crew if m.years_experience >= 5]
            if len(experienced) < len(self.crew) / 2:
                raise ValueError("Long missions require at least 50% experienced crew")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def demo():
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=45,
                    specialization="Mission Command",
                    years_experience=15
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=34,
                    specialization="Navigation",
                    years_experience=8
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=29,
                    specialization="Engineering",
                    years_experience=6
                ),
            ]
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for m in valid_mission.crew:
            print(f"- {m.name} ({m.rank}) - {m.specialization}")

    except ValidationError as e:
        print(e)

    print("=" * 40)

    # Invalid mission (no commander/captain)
    try:
        invalid_mission = SpaceMission(
            mission_id="M12345",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime.now(),
            duration_days=100,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="C004",
                    name="Bob Lee",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=3
                )
            ]
        )

    except ValidationError as e:
        print("Expected validation error:")
        print(e)


# Run demo
if __name__ == "__main__":
    demo()