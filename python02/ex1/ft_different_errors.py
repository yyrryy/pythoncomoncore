def garden_operations(error_type):
    if error_type == "value":
        int("abc")

    elif error_type == "zero":
        10 / 0

    elif error_type == "file":
        f = open("missing.txt", "r")
        f.close()

    elif error_type == "key":
        plants = {"name": "abdelouahed", "age": 10}
        print(plants["height"])


def test_error_types():
    print("=== Garden Error Types Demo ===")
    try:
        print("Testing ValueError")
        garden_operations("value")
    except ValueError as e:
        print(f"Caught Error: {e}, the program continues \n")

    # ZeroDivisionError
    try:
        print("Testing ZeroDivisionError")
        garden_operations("zero")
    except ZeroDivisionError as e:
        print(f"Caught Error: {e}, the program continues \n")

    # FileNotFoundError
    try:
        print("Testing FileNotFoundError...")
        garden_operations("file")
    except FileNotFoundError as e:
        print(f"Caught Error: {e}, the program continues \n")

    # KeyError
    try:
        print("Testing KeyError...")
        garden_operations("key")
    except KeyError as e:
        print(f"Caught Error: {e}, the program continues \n")

    try:
        print("Testing multiple errors together...")
        garden_operations("value")
        garden_operations("key")
        garden_operations("file")
        garden_operations("zero")
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
        print("Caught all error, the program continues \n")
    garden_operations(None)
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
