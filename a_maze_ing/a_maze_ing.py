import sys
import os
from typing import List, Tuple
from time import sleep
from mazegen import MazeGenerator, read_file, InvalideValue,  _42cells
try:
    COLORS = [
        "\033[97m",  # White
        "\033[92m",  # Green
        "\033[94m",  # Blue
        "\033[93m",  # Yellow
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
        "\033[31m",  # Red
    ]

    def clear_screen() -> None:
        """
        Clear the terminal screen.

        Uses 'clear' on Unix-like systems and 'cls' on Windows.
        """
        os.system("clear" if os.name != "nt" else "cls")

    color_index = 0

    def print_file(file_path: str, delay: float, color: str) -> None:
        """
        Print the contents of a file to the terminal with animated typing.

        Args:
            file_path (str): Path to the file to display.
            delay (float): Delay between characters when printing.
            color (str): Terminal color used for the output.
        """
        clear_screen()

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    sys.stdout.write(color)

                    for char in line:
                        sys.stdout.write(char)
                        sys.stdout.flush()
                        sleep(delay)

                    sys.stdout.write("\033[0m")  # reset color
                    sys.stdout.flush()
        except PermissionError:
            raise PermissionError(f"No reading permission in {file_path}")
        except FileNotFoundError:
            raise FileNotFoundError(f"{file_path} is not found")
    fixed_seed_flag = False
    try:
        config = read_file()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        start = config["ENTRY"]
        perfect = config["PERFECT"]
        end = config["EXIT"]
        output_file = config["OUTPUT_FILE"]
        try:
            seed = config["SEED"]
            fixed_seed_flag = True
        except Exception:
            seed = None

    except (InvalideValue, ValueError) as e:
        print(e)
        sys.exit(1)

    print_file("paint_maze.txt", delay=0.003, color="\033[92m")

    clear_screen()
    print_file("paint_maze.txt", 0, "\033[92m")
    sleep(1.5)
    maze = MazeGenerator(
        width, height, perfect, start, end, output_file, fixed_seed_flag,
        seed)
    # try:
    grid = maze.create_grid()
    maze.generate_maze(grid)
    maze.print_maze(grid, start, end, [], COLORS[color_index])
    maze.solve_maze(grid, True)
    path: List[Tuple[int, int]] = []
    show_path = False
    while True:
        print("\n")
        print("═" * 52)
        print("║{:^50}║".format("A-Maze-ing"))
        print("╠" + "═" * 50 + "╣")
        print("║ {:<48} ║".format("1. Re-generate a new maze"))
        print("║ {:<48} ║".format("2. Show/Hide path from entry to exit"))
        print("║ {:<48} ║".format("3. Rotate maze colors"))
        a = 'fixed' if fixed_seed_flag else 'unfixed'
        b = 'unfix it' if fixed_seed_flag else 'fix it'
        print("║ {:<48} ║" .format(f"4. Seed is {a} in config file, {b}"))
        print("║ {:<48} ║".format("5. Change Exit in config file"))
        print("║ {:<48} ║".format("6. Change Entry in config file"))
        print("║ {:<48} ║".format("7. Quit"))
        print("╚" + "═" * 50 + "╝")

        try:
            str_choice = input("Choice? (1-6): ")
            try:
                choice = int(str_choice)
            except ValueError:
                print("Not valid input !")
                break

            if choice == 1:
                clear_screen()
                print_file("paint_maze.txt", 0, "\033[92m")
                try:
                    config = read_file()
                    width = config["WIDTH"]
                    height = config["HEIGHT"]
                    start = config["ENTRY"]
                    perfect = config["PERFECT"]
                    end = config["EXIT"]
                    output_file = config["OUTPUT_FILE"]
                    try:
                        seed = config["SEED"]
                    except Exception:
                        seed = None

                except (InvalideValue, ValueError) as e:
                    print(e)
                    sys.exit(1)
                maze = MazeGenerator(
                    width,
                    height,
                    perfect,
                    start,
                    end,
                    output_file,
                    fixed_seed_flag,
                    seed
                )
                # try:
                grid = maze.create_grid()
                maze.generate_maze(grid)
                maze.print_maze(grid, start, end, [], COLORS[color_index])
                maze.solve_maze(grid, True)
                path = []
                show_path = False
            elif choice == 2:
                clear_screen()
                print_file("paint_maze.txt", 0, "\033[94m")
                show_path = not show_path
                if show_path:
                    path = maze.solve_maze(grid, False)
                else:
                    path = []
                print(f"\nCurrent maze seed: {maze.seed}")
                maze.print_maze(grid, start, end, path, COLORS[color_index])

            elif choice == 3:
                clear_screen()
                if show_path:
                    path = maze.solve_maze(grid, False)
                else:
                    path = []
                color_index = (color_index + 1) % len(COLORS)
                print_file("paint_maze.txt", 0, COLORS[color_index])
                print(f"\nCurrent maze seed: {maze.seed}")
                maze.print_maze(grid, start, end, path, COLORS[color_index])

            elif choice == 7:
                print_file("exit.txt", delay=0.001, color="\033[31m")
                break
            elif choice == 4:
                fixed_seed_flag = not fixed_seed_flag
                maze.fix_seed()
                clear_screen()
                try:
                    config = read_file()
                    width = config["WIDTH"]
                    height = config["HEIGHT"]
                    start = config["ENTRY"]
                    perfect = config["PERFECT"]
                    end = config["EXIT"]
                    output_file = config["OUTPUT_FILE"]
                    try:
                        seed = config["SEED"]
                    except Exception:
                        seed = None

                except (InvalideValue, ValueError) as e:
                    print(e)
                    sys.exit(1)
                maze = MazeGenerator(
                    width,
                    height,
                    perfect,
                    start,
                    end,
                    output_file,
                    fixed_seed_flag,
                    seed
                )
                # try:
                print_file("paint_maze.txt", 0, COLORS[color_index])
                grid = maze.create_grid()
                maze.generate_maze(grid)
                maze.print_maze(grid, start, end, [], COLORS[color_index])
                maze.solve_maze(grid, True)
                path = []
                show_path = False
            elif choice == 5:
                try:
                    show_path = False
                    width = maze.width
                    height = maze.height
                    coords_str = input("Enter exit coordinations [x,y]: ")
                    coords = coords_str.split(",")
                    try:
                        x, y = int(coords[0]), int(coords[1])
                    except Exception:
                        raise ValueError("please provide x,y coordinations")
                    if 0 < x > width or 0 < y > height:
                        print("Coordinations are out of maze")
                        break
                    if (x, y) in _42cells(width, height):
                        print("Coordinations are in 42 cells")
                        break
                    if x == start[0] and y == start[1]:
                        print("Coordinations must be different than the entry")
                        break
                    else:
                        try:
                            with open("config.txt", "w") as file:
                                print(
                                    f"""WIDTH={width}
HEIGHT={maze.height}
ENTRY={maze.start[0]},{maze.start[1]}
EXIT={x},{y}
perFect={maze.isperfect}
OUTPUT_FILE={maze.output_file}\n""",
                                    file=file,
                                )
                            if fixed_seed_flag:
                                with open("config.txt", "a") as file:
                                    print(f"SEED={maze.seed}", file=file)
                        except PermissionError:
                            print("No permission to open the config file")
                    try:
                        config = read_file()
                        width = config["WIDTH"]
                        height = config["HEIGHT"]
                        start = config["ENTRY"]
                        perfect = config["PERFECT"]
                        end = config["EXIT"]
                        output_file = config["OUTPUT_FILE"]
                        try:
                            seed = config["SEED"]
                        except Exception:
                            seed = None

                    except (InvalideValue, ValueError) as e:
                        print(e)
                        sys.exit(1)
                    clear_screen()
                    maze = MazeGenerator(
                        width,
                        height,
                        perfect,
                        start,
                        end,
                        output_file,
                        fixed_seed_flag,
                        seed
                    )
                    # try:
                    print_file("paint_maze.txt", 0, COLORS[color_index])
                    grid = maze.create_grid()
                    maze.generate_maze(grid)
                    maze.print_maze(grid, start, end, [], COLORS[color_index])
                    maze.solve_maze(grid, True)
                except (ValueError, KeyboardInterrupt) as e:
                    print("\nInput is not valid, Exiting", e)
                    break
                except Exception as e:
                    print("An unexpected error", e)
            elif choice == 6:
                try:
                    show_path = False
                    width = maze.width
                    height = maze.height
                    coords_str = input("Enter entry coordinations [x,y]: ")
                    coords = coords_str.split(",")
                    try:
                        x, y = int(coords[0]), int(coords[1])
                    except Exception:
                        raise ValueError("please provide x,y coordinations")
                    if 0 < x > width or 0 < y > height:
                        print("Coordinations are out of maze")
                        break
                    if (x, y) in _42cells(width, height):
                        print("Coordinations are in 42 cells")
                        break
                    if x == end[0] and y == end[1]:
                        print("Coordinations must be different than the entry")
                        break
                    else:
                        try:
                            with open("config.txt", "w") as file:
                                print(
                                    f"""WIDTH={width}
HEIGHT={maze.height}
ENTRY={x},{y}
EXIT={maze.end[0]},{maze.end[1]}
perFect={maze.isperfect}
OUTPUT_FILE={maze.output_file}\n""",
                                    file=file,
                                )
                            if fixed_seed_flag:
                                with open("config.txt", "a") as file:
                                    print(f"SEED={maze.seed}", file=file)
                        except PermissionError:
                            print("No permission to open the config file")
                    try:
                        config = read_file()
                        width = config["WIDTH"]
                        height = config["HEIGHT"]
                        start = config["ENTRY"]
                        perfect = config["PERFECT"]
                        end = config["EXIT"]
                        output_file = config["OUTPUT_FILE"]
                        try:
                            seed = config["SEED"]
                        except Exception:
                            seed = None

                    except (InvalideValue, ValueError) as e:
                        print(e)
                        sys.exit(1)
                    clear_screen()
                    maze = MazeGenerator(
                        width,
                        height,
                        perfect,
                        start,
                        end,
                        output_file,
                        fixed_seed_flag,
                        seed
                    )
                    # try:
                    print_file("paint_maze.txt", 0, COLORS[color_index])
                    grid = maze.create_grid()
                    maze.generate_maze(grid)
                    maze.print_maze(grid, start, end, [], COLORS[color_index])
                    maze.solve_maze(grid, True)
                except (ValueError, KeyboardInterrupt) as e:
                    print("\nInput is not valid, Exiting", e)
                    break
                except Exception as e:
                    print("An unexpected error", e)
            else:
                print("Not valid input !")
                break
        except (KeyboardInterrupt, EOFError):
            break
except Exception as e:
    print(e)
