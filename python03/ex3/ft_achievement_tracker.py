# Sample player achievements
player_achievements = {
    "alice": {"first_kill", "level_10", "treasure_hunter", "speed_demon"},
    "bob": {"first_kill", "level_10", "boss_slayer", "collector"},
    "charlie": {"level_10", "treasure_hunter", "boss_slayer", "speed_demon", "perfectionist"}
}

print("=== Achievement Tracker System ===")
for player, achievements in player_achievements.items():
    print(f"Player {player} achievements: {achievements}")

# === Achievement Analytics ===
# All unique achievements
all_achievements = set().union(*player_achievements.values())
print("\n=== Achievement Analytics ===")
print("All unique achievements:", all_achievements)
print("Total unique achievements:", len(all_achievements))

# Common achievements to all players
common_all = set.intersection(*player_achievements.values())
print("Common to all players:", common_all)

# Rare achievements (appear in only 1 player)
rare_achievements = {ach for ach in all_achievements if sum(ach in p for p in player_achievements.values()) == 1}
print("Rare achievements (1 player):", rare_achievements)

# Pairwise analysis: Alice vs Bob
alice_vs_bob_common = player_achievements["alice"] & player_achievements["bob"]
print("Alice vs Bob common:", alice_vs_bob_common)

alice_unique = player_achievements["alice"] - player_achievements["bob"]
bob_unique = player_achievements["bob"] - player_achievements["alice"]
print("Alice unique:", alice_unique)
print("Bob unique:", bob_unique)