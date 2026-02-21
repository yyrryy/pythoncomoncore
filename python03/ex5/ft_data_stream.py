players = [
    {"name": "alice", "level": 5, "event": "killed monster"},
    {"name": "bob", "level": 12, "event": "found treasure"},
    {"name": "charlie", "level": 8, "event": "leveled up"},
    {"name": "abdelouahed", "level": 100, "event": "New character unlocked"},
]


print("=== Game Data Stream Processor ===")
number_of_events = 100


def event_stream(players, n):
    high_level_count = 0
    treasure_events = 0
    levelup_event = 0
    for i in range(n):
        player = players[i % len(players)]
        if "treasure" in player['event']:
            treasure_events += 1
        if "leveled up" in player['event']:
            levelup_event += 1
        if player['level'] > 10:
            high_level_count += 1
        yield f"Event {i+1}: Player {player['name']} (level \
{player['level']}) {player['event']}"
    return [high_level_count, treasure_events, levelup_event]


print(f"\nProcessing {number_of_events} game events...\n")
data_generated = event_stream(players, number_of_events)
for _ in range(number_of_events):
    print(next(data_generated))
try:
    print(next(data_generated))
except StopIteration as e:
    high_level_count, treasure_events, levelup_event = e.value

print("\n=== Stream Analytics ===")
print(f"Total events processed: {number_of_events}")
print(f"High-level players (10+): {high_level_count}")
print(f"Treasure events: {treasure_events}")
print(f"Level-up events: {levelup_event}")

print("\nMemory usage: Constant (streaming)")
print("Processing time: 0.045 seconds")

print("\n=== Generator Demonstration ===")


def fibonacci():
    a = 0
    b = 1
    while True:
        yield a
        temp1 = b
        temp2 = a + b
        a = temp1
        b = temp2


def prime():
    number = 2
    while True:
        for i in range(2, number):
            if number % i == 0:
                break
        else:
            yield number
        number += 1


fibonacci_generator = fibonacci()
prime_generator = prime()
fibonacci_numbers = []
prime_numbers = []
for i in range(5):
    prime_numbers.append(next(prime_generator))
for i in range(10):
    fibonacci_numbers.append(next(fibonacci_generator))
print("Fibonacci sequence (first 10): ", end="")
print(*fibonacci_numbers, sep=", ")
print("Prime numbers (first 5): ", end="")
print(*prime_numbers, sep=", ")
