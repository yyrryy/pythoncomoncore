import alchemy
print("=== Sacred Scroll Mastery ===")
print("Testing direct module access:")
print("alchemy.elements.create_fire()", alchemy.elements.create_fire())
print("alchemy.elements.create_water()", alchemy.elements.create_water())
print("alchemy.elements.create_earth()", alchemy.elements.create_earth())
print("alchemy.elements.create_air()", alchemy.elements.create_air())
print()
print("Testing package-level access (controlled by __init__.py):")
print("alchemy.create_fire()", alchemy.create_fire())
print("alchemy.create_water()", alchemy.create_water())
printing = ""
try:
    printing = alchemy.create_earth()
except AttributeError:
    printing = "AttributeError - not exposed"
print("alchemy.create_earth()", printing)
printing = ""
try:
    printing = alchemy.create_air()
except AttributeError:
    printing = "AttributeError - not exposed"
print("alchemy.create_air()", alchemy.create_air())
print("Package metadata:")
print("Version:", alchemy.__version__)
print("Author:", alchemy.__author__)
