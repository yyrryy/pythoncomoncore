from abc import ABC, abstractmethod
from enum import Enum


class Rarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class Card (ABC):
    def __init__(self, name: str, cost: int, rarity: str):
        self.name = name
        self.cost = cost
        if rarity not in [i.values for i in Rarity]:
            raise ValueError("Rarity is invalid")
        self.rarity = rarity

    def play(self, game_state: dict) -> dict:
        pass
    play = abstractmethod(play)

    def get_card_info(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity
        }

    def is_playable(self, available_mana: int) -> bool:
        return available_mana >= self.cost
