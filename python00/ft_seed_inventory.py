def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    after_unit = ""
    if unit == "grams":
        after_unit = "grams total"
    elif unit == "packets":
        after_unit = "packets available"
    elif unit == "area":
        after_unit = "square meters"
    else:
        after_unit = "Unknown unit type"
    print(seed_type.capitalize(), "seeds: ", quantity, after_unit)
