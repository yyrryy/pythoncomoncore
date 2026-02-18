#Authorized: dict(), len(), print(), keys(), values(), items(), get(),update(), sys, sys.argv
# sort items before storing in dict
import sys
if __name__ == '__main__':
    args = sys.argv[1:]
    inventory_data = dict()
    sum_quantities = 0
    for i in args:
        key, value = i.split(':')
        try:
            value = int(value)
        except ValueError as e:
            #finish this
            pass
        inventory_data[key] = value
        sum_quantities += value
    unique_items = len(set(inventory_data.keys()))
    print("=== Inventory System Analysis ===")
    print("Total items in inventory:", sum_quantities)
    print("Unique item types:", unique_items)
    print("\n=== Current Inventory ===")
    for key, value in inventory_data.items():
        percentage = round((value/sum_quantities)*100, 1)
        print(f"{key}: {value} units ({percentage}%)")
    print("\n=== Inventory Statistics ===")
    #finish this
    print("\n=== Item Categories ===")
    #finish this
    print("\n=== Management Suggestions ===")
    #finish this
    print("\n=== Dictionary Properties Demo ===")
    print(f"Dictionary keys: {inventory_data.keys()}")
    print(f"Dictionary values: {inventory_data.values()}")
    item_to_lookup = 'sword'
    print(f"Sample lookup - '{item_to_lookup}' in inventory: {item_to_lookup in inventory_data.keys()}")