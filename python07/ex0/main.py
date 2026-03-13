from .Card import Card
from .CreatureCard import CreatureCard

print("\n=== DataDeck Card Foundation ===\n")

print("Testing Abstract Base Class Design:\n")

print("CreatureCard Info:")
creature = CreatureCard('Fire Dragon', 5, 'Legendary', 7, 5)
print(creature.get_details())

creature.play({"mana": 6})
print("Attack result:", creature.attack_target("Goblin Warrior"))

print("\nTesting insufficient mana (3 available):")
creature.play({"mana": 3})

print("\nAbstract pattern successfully demonstrated!")
