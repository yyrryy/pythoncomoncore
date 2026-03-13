from ex0.Card import Card


class CreatureCard (Card):
    def __init__(self, name: str, cost: int, rarity: str, attack: int, health: int):
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        if self.is_playable(game_state["mana"]):
            print(f"\nPlaying {self.name} with {game_state['mana']} mana available:")
            print("playable: True")
            response = {
                "card_played": self.name,
                "mana_used": self.cost,
                "effect": "Creature summoned to battlefield"
            }
            print("Play result:", response)
            return response
        else:
            print("playable: False")

    def attack_target(self, target) -> dict:
        print(f"\n{self.name} attacks {target}:")
        return {
            'attacker': self.name,
            'target': target,
            'damage_dealt': self.attack,
            'combat_resolved': True
        }

    def get_details(self) -> dict:
        response = super().get_card_info()
        response["type"] = "creature"
        response["attack"] = self.attack
        response["health"] = self.health
        return response
