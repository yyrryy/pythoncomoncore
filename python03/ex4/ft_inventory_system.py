import sys

if __name__ == '__main__':
    try:
        args = sys.argv[1:]
        inventory_data = dict()
        sum_quantities = 0
        for i in args:
            key, value = i.split(':')
            try:
                value = int(value)
            except ValueError as e:
                print(f"Errpr processing {key}: {e}")
            inventory_data[key] = value
            sum_quantities += value
        unique_items = len(set(inventory_data.keys()))
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
            percentage = round((value / sum_quantities) * 100, 1)
            print(f"{key}: {value} units ({percentage}%)")
            if i != len(items)-1:
                dict_keys += key + ", "
                dict_values += str(value) + ", "
            else:
                dict_keys += key
                dict_values += str(value)
            if value > max_value:
                max_value = value
                min_value = value
                max_key = key
            if value < min_value:
                min_value = value
                min_key = key
            if value < 2:
                restock_needed.append(key)
        
        print("\n=== Inventory Statistics ===")
        print(f"Most abundant: {max_key} ({max_value} units)")
        print(f"Least abundant: {min_key} ({min_value} "
              f"unit{'s' if min_value != 1 else ''})")
        print("\n=== Item Categories ===")
        moderate = dict()
        scarce = dict()
        for key, value in inventory_data.items():
            if value >= max_value:
                moderate.update({key: value})
            else:
                scarce.update({key: value})
        print(f"Moderate: {moderate}")
        print(f"Scarce: {scarce}")

        print("\n=== Management Suggestions ===")
        print("Restock needed: ", end="")
        print(*restock_needed, sep=", ")
        print("\n=== Dictionary Properties Demo ===")
        print(f"Dictionary keys: {dict_keys}")
        print(f"Dictionary values: {dict_values}")
        item_to_lookup = 'sword'
        print(f"Sample lookup - '{item_to_lookup}' in inventory: "
              f"{item_to_lookup in inventory_data.keys()}")
    except Exception as e:
        print(f"An unexpected error happened: {e}")
