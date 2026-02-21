import math

# Create a fixed position
position = (10, 20, 5)
print("Position created:", position)

# Distance from origin
x, y, z = position
distance = math.sqrt(x**2 + y**2 + z**2)
print(f"Distance between (0,0,0) and {position}: {distance:.2f}")

# Parsing a coordinate string
coord_str = "3,4,0"
try:
    parsed_position = tuple(int(c) for c in coord_str.split(','))
    print("Parsed position:", parsed_position)
    px, py, pz = parsed_position
    print(f"Distance between (0,0,0) and {parsed_position}: {math.sqrt(px**2 + py**2 + pz**2):.2f}")
except ValueError as e:
    print(f"Error parsing coordinates: {e}")
    print("Error details - Type:", type(e), "Args:", e.args)