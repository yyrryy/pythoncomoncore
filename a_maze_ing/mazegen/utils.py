from typing import List, Tuple
from .cell import Cell


def _42cells(
        maze_width: int,
        maze_height: int
                        ) -> List[Tuple[int, int]]:
    """
    Return a list of coordinates forming the "42" pattern in the maze.

    This function computes a fixed set of cells
    relative to the center of the maze,
    typically used for special marking or
    visualization purposes (e.g., highlighting
    these cells in green in the printed maze).

    Args:
        maze_width (int): The width of the maze grid.
        maze_height (int): The height of the maze grid.

    Returns:
        List[Tuple[int, int]]: A list of (x, y) coordinates for the "42" cells.
    """
    cells = [
        ((maze_width // 2) + 2, (maze_height // 2) - 2),
        ((maze_width // 2) + 1, (maze_height // 2) - 2),
        ((maze_width // 2) + 3, (maze_height // 2) - 2),
        ((maze_width // 2) + 3, (maze_height // 2) - 1),
        ((maze_width // 2) + 3, (maze_height // 2)),
        ((maze_width // 2) + 2, (maze_height // 2)),
        ((maze_width // 2) + 1, (maze_height // 2)),
        ((maze_width // 2) + 1, (maze_height // 2) + 1),
        ((maze_width // 2) + 1, (maze_height // 2) + 2),
        ((maze_width // 2) + 2, (maze_height // 2) + 2),
        ((maze_width // 2) + 3, (maze_height // 2) + 2),
        \
        ((maze_width // 2) - 3, (maze_height // 2) - 2),
        ((maze_width // 2) - 3, (maze_height // 2) - 1),
        ((maze_width // 2) - 3, (maze_height // 2)),
        ((maze_width // 2) - 2, (maze_height // 2)),
        ((maze_width // 2) - 1, (maze_height // 2)),
        ((maze_width // 2) - 1, (maze_height // 2) + 1),
        ((maze_width // 2) - 1, (maze_height // 2) + 2)
    ]
    return cells


def reset_cells(grid: List[List[Cell]], width: int, height: int) -> None:
    """
    Reset the state of all cells in the grid.

    Sets `isvisited` and `is42` flags of every cell to False, except for
    the cells forming the "42" pattern,
    which are marked as visited (`isvisited=True`)
    and flagged as `is42=True`.

    Args:
        grid (List[List[Cell]]): The 2D grid of Cell objects to reset.
        width (int): Width of the maze/grid.
        height (int): Height of the maze/grid.
    """
    cells_42 = _42cells(width, height)
    for cells_in_grid in grid:
        for cell in cells_in_grid:
            x, y = cell.x, cell.y
            cell.isvisited = False
            cell.is42 = False
            if (x, y) in cells_42:
                cell.isvisited = True
                cell.is42 = True


def get_neighbors(grid: List[List[Cell]], current_cell: Cell,
                  width: int, height: int) -> List[Tuple[str, Cell]]:
    """
    Get all unvisited neighboring cells of the current cell.

    For each cardinal direction (North, South, East, West), the function
    checks if the neighboring cell is inside the grid boundaries and
    has not been visited. Valid neighbors are returned along with their
    direction relative to the current cell.

    Args:
        grid (List[List[Cell]]): 2D grid of Cell objects representing the maze.
        current_cell (Cell): The cell whose neighbors are being checked.
        width (int): Width of the grid.
        height (int): Height of the grid.

    Returns:
        List[Tuple[str, Cell]]: A list of tuples, each containing a direction
        ('N', 'S', 'E', 'W') and the corresponding unvisited neighboring Cell.

    Notes:
        - Only unvisited cells are returned.
        - Coordinates are validated to ensure neighbors are within the grid.
    """
    neighbors = []

    this_cell_x = current_cell.x
    this_cell_y = current_cell.y

    directions = [
        ("N", 0, -1),
        ("S", 0, 1),
        ("E", 1, 0),
        ("W", -1, 0),
    ]

    for direction, x, y in directions:
        next_x = this_cell_x + x
        next_y = this_cell_y + y

        if 0 <= next_x < width and 0 <= next_y < height:
            neighbor = grid[next_y][next_x]
            if not neighbor.isvisited:
                neighbors.append((direction, neighbor))
    return neighbors


def get_path(path: dict, grid: list,
             output_file: str,
             print_to_file: bool,
             color: str = "\033[97m") -> List[Tuple[int, int]]:
    """
    Reconstruct the solution path from a BFS/DFS parent dictionary.

    The function traces back from the cell marked as part of the solution
    (`is_solution=True`) using the 'parent' links in the `path` dictionary.
    It optionally prints the sequence of directions to a file.

    Args:
        path (dict): A dictionary mapping cell coordinates to metadata:
            {
                "parent": Tuple[int, int] | None,
                "is_solution": bool,
                "direction": str | None
            }
        grid (list): 2D grid of Cell objects
        (used for reference; not modified).
        output_file (str): Path to a file where
        the directions of the solution path
        will be written if `print_to_file` is True.
        print_to_file (bool): Whether to print
        the solution directions to a file.
        color (str, optional): ANSI escape code
        for terminal color. Defaults to white.

    Returns:
        List[Tuple[int, int]]: Ordered list of
        cell coordinates representing the
        solution path from start to goal.

    Notes:
        - The path is reconstructed in reverse
        using parent pointers and then reversed
          to provide start-to-end order.
        - Directions are optionally written to
        the output file in the order of traversal.
    """
    solution_key = None
    for key, value in path.items():
        if value["is_solution"]:
            solution_key = key
    real_path = []
    real_direction = []
    current = solution_key
    current_direction = path[solution_key]["direction"]
    while current is not None:
        real_path.append(current)
        if current_direction:
            real_direction.append(current_direction)
            current_direction = path[current]["direction"]
        current = path[current]["parent"]
    if print_to_file:
        with open(output_file, "a") as f:
            real_direction.reverse()
            print(*real_direction, sep="", file=f)
    real_path.reverse()
    return real_path


def print_hexa(output_file: str, grid: List[List[Cell]], start: Tuple,
               end: Tuple) -> None:
    """
    Write the maze to a file in hexadecimal format.

    Each cell in the grid is converted to a single hexadecimal digit
    representing its walls using `Cell.get_value()`. The resulting grid
    is written row by row. After the grid, the start and end coordinates
    are appended.

    Args:
        output_file (str): Path to the output file.
        grid (List[List[Cell]]): 2D grid of Cell objects representing the maze.
        start (Tuple[int, int]): Coordinates of the starting cell.
        end (Tuple[int, int]): Coordinates of the ending cell.

    Side Effects:
        - Writes the hexadecimal representation of the maze to `output_file`.
        - Appends start and end coordinates at the end of the file.
    """
    try:
        with open(output_file, "w") as f:
            for cells in grid:
                for cell in cells:
                    value = cell.get_value()
                    f.write(f"{value:X}")  # Direct hex formatting
                f.write("\n")
            f.write("\n")
            f.write(f"{start[0]},{start[1]}")
            f.write("\n")
            f.write(f"{end[0]},{end[1]}")
            f.write("\n")
    except FileNotFoundError:
        raise FileNotFoundError("the output file is not found")
    except PermissionError:
        raise PermissionError("the output file has no reading permession")
