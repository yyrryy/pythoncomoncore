import sys

if __name__ == "__main__":
    print("=== Command Quest ===")
    args = sys.argv
    argumants_count = len(args) - 1
    if argumants_count == 0:
        print("No arguments provided!")
        print(f"Program name: {args[0]}")
        print(f"Total arguments: {argumants_count + 1}")
    else:
        print(f"Program name: {args[0]}")
        print(f"Arguments received: {argumants_count}")
    if argumants_count + 1 > 1:
        i = 0
        while i < argumants_count:
            print(f"Argument {i+1}: {args[i+1]}")
            i += 1
    print(f"Total arguments: {argumants_count + 1}")
