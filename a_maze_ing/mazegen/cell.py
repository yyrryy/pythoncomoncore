
class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.isvisited = False
        self.is42 = False
        self.walls = {"N": True, "E": True, "S": True, "W": True}

    def remove_walls(self, neighbor: 'Cell', direction: str) -> None:
        """
        Remove the wall between the current cell and a neighboring cell.

        The wall in the given direction of the current cell is set to False,
        and the opposite wall of the neighbor cell is also set to False.

        Args:
            neighbor (Cell): The neighboring cell.
            direction (str): Direction of the neighbor
            relative to the current cell.
        """
        if direction == "N":
            self.walls["N"] = False
            neighbor.walls["S"] = False
        elif direction == "S":
            self.walls["S"] = False
            neighbor.walls["N"] = False
        elif direction == "E":
            self.walls["E"] = False
            neighbor.walls["W"] = False
        elif direction == "W":
            self.walls["W"] = False
            neighbor.walls["E"] = False

    def get_value(self) -> int:
        """
        Compute the decimal value of the cell based on its walls.

        Each wall direction corresponds to a bit position. If a wall is present
        (True), the corresponding bit is set using a left shift operation.

        Example:
            walls = {"N": True, "E": True, "S": False, "W": True}

            N -> 1 << 0 = 1
            E -> 1 << 1 = 2
            S -> no wall (0)
            W -> 1 << 3 = 8

            cell value = 1 + 2 + 8 = 11

        Returns:
            int: The decimal representation of the cell walls.
        """
        value = 0
        count = 0
        for direction in self.walls:
            closed = self.walls[direction]
            value += closed << count
            count += 1
        return value
