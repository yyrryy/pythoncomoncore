import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    inventory_data = {}
    sum_quantities = 0
    for i in args:
        try:
            key, value = i.split(':')
        except ValueError as e:
            print("ERROR cought:", e)
            continue
        try:
            value = int(value)
        except ValueError as e:
            print(f"Errpr processing {key}: {e}")
        inventory_data[key] = {"quantity": value}
        sum_quantities += value
    unique_items = len(set(inventory_data.keys()))
    # print(inventory_data)
    dict_keys = ""
    dict_values = ""
    print("=== Inventory System Analysis ===")
    print("Total items in inventory:", sum_quantities)
    print("Unique item types:", unique_items)
    print("\n=== Current Inventory ===")
    dict_keys = ""
    dict_values = ""
    items = list(inventory_data.items())
    max_value = 0
    min_value = 0
    max_key = ""
    min_key = ""
    restock_needed = []
    for i in range(len(items)):
        key, value = items[i]
        percentage = round((value["quantity"] / sum_quantities) * 100, 1)
        quantity = value["quantity"]
        print(f"{key}: {quantity} units ({percentage}%)")
        if i != len(items)-1:
            dict_keys += key + ", "
            dict_values += str(value["quantity"]) + ", "
        else:
            dict_keys += key
            dict_values += str(value["quantity"])
        if value["quantity"] > max_value:
            max_value = value["quantity"]
            min_value = value["quantity"]
            max_key = key
    for i in range(len(items)):
        key, value = items[i]
        if value["quantity"] < min_value:
            min_value = value["quantity"]
            min_key = key
        if value["quantity"] < 2:
            restock_needed.append(key)
    
    print("\n=== Inventory Statistics ===")
    print(f"Most abundant: {max_key} ({max_value} units)")
    print(f"Least abundant: {min_key} ({min_value} "
          f"unit{'s' if min_value != 1 else ''})")
    print("\n=== Item Categories ===")
    moderate = {}
    scarce = {}

    for key, value in inventory_data.items():
        if value["quantity"] >= max_value:
            inventory_data[key]["category"] = "moderate"
            moderate[key] = value["quantity"]
        else:
            inventory_data[key]["category"] = "scarce"
            scarce[key] = value["quantity"]
    
    print("Moderate:", moderate)
    print("Scarce:", scarce)
    item_to_lookup = 'sword'
    print(f"Sample lookup - '{item_to_lookup}' in inventory: "
          f"{item_to_lookup in inventory_data.keys()}")
