# Sample data
players = [
    {"name": "alice", "score": 2300, "achievements": ["first_kill", "level_10", "boss_slayer", "treasure_hunt", "puzzle_master"], "region": "north"},
    {"name": "bob", "score": 1800, "achievements": ["first_kill", "puzzle_master", "level_5"], "region": "east"},
    {"name": "charlie", "score": 2150, "achievements": ["level_10", "boss_slayer", "treasure_hunt", "speed_runner", "puzzle_master", "first_kill", "level_15"], "region": "north"},
    {"name": "diana", "score": 2050, "achievements": ["boss_slayer", "treasure_hunt", "first_kill"], "region": "central"}
]

print("=== Game Analytics Dashboard ===\n")

# === List Comprehension Examples ===
high_scorers = [p["name"] for p in players if p["score"] > 2000]
scores_doubled = [p["score"] * 2 for p in players]
active_players = [p["name"] for p in players if len(p["achievements"]) >= 3]

print("=== List Comprehension Examples ===")
print("High scorers (>2000):", high_scorers)
print("Scores doubled:", scores_doubled)
print("Active players:", active_players)
print()

# === Dict Comprehension Examples ===
player_scores = {p["name"]: p["score"] for p in players}
score_categories = {
    "high": len([p for p in players if p["score"] > 2000]),
    "medium": len([p for p in players if 1500 <= p["score"] <= 2000]),
    "low": len([p for p in players if p["score"] < 1500])
}
achievement_counts = {p["name"]: len(p["achievements"]) for p in players}

print("=== Dict Comprehension Examples ===")
print("Player scores:", player_scores)
print("Score categories:", score_categories)
print("Achievement counts:", achievement_counts)
print()

# === Set Comprehension Examples ===
unique_players = {p["name"] for p in players}
unique_achievements = {ach for p in players for ach in p["achievements"]}
active_regions = {p["region"] for p in players}

print("=== Set Comprehension Examples ===")
print("Unique players:", unique_players)
print("Unique achievements:", unique_achievements)
print("Active regions:", active_regions)
print()

# === Combined Analysis ===
total_players = len(players)
total_unique_achievements = len(unique_achievements)
average_score = sum(p["score"] for p in players) / total_players

# Top performer
top_player = max(players, key=lambda p: p["score"])
top_name = top_player["name"]
top_score = top_player["score"]
top_achievements = len(top_player["achievements"])

print("=== Combined Analysis ===")
print("Total players:", total_players)
print("Total unique achievements:", total_unique_achievements)
print("Average score:", average_score)
print(f"Top performer: {top_name} ({top_score} points, {top_achievements} achievements)")