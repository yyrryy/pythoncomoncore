*This project has been created as part of the 42 curriculum by `yobouaji`, `aaliali`.*

# A-MAZE-ING

## Description

**A-MAZE-ING** is a maze generation and visualization program developed for the 42 curriculum.

It:
- Reads maze settings from a configuration file
- Generates a maze
- Displays the maze in the terminal (colored output)
- Can solve the maze and optionally display the solution path
- Exports the maze as a **hexadecimal-encoded grid** to an output file

The project also contains a reusable Python package, **`mazegen`**, so the generation/solving/printing/export logic can be imported and reused in other projects.

---

## Instructions

### Requirements

- Python **3.10+**
- `pip`

(Optional)
- `make` (if you use the Makefile targets)

### Installation

Using `pip`:

```bash
pip3 install -r reqs.txt
```

Or using the Makefile:

```bash
make install
```

### Execution

Run:

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

### Interactive controls (in-program menu)

When the program starts, you can:
1. Re-generate a new maze
2. Show/Hide the path from entry to exit
3. Rotate maze colors
4. Fix/Unfix seed (deterministic generation)
5. Change Exit (updates the config file and regenerates)
6. Quit

### Debugging

```bash
make debug
```

### Linting

```bash
make lint
```

---

## Configuration file (complete format)

The program uses a config file made of **KEY=VALUE** lines.

### Full structure

```text
WIDTH=<int>
HEIGHT=<int>
ENTRY=<x>,<y>
EXIT=<x>,<y>
PERFECT=<true|false>
OUTPUT_FILE=<path>
SEED=<int>               (optional)
```

### Example

```text
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
PERFECT=true
OUTPUT_FILE=output_maze.txt
SEED=100
```

### Parameters details

- `WIDTH` / `HEIGHT`: maze dimensions
- `ENTRY`: entry cell coordinates as `x,y`
- `EXIT`: exit cell coordinates as `x,y`
- `PERFECT`:
  - `true` => perfect maze (unique path between any two cells)
- `OUTPUT_FILE`: where the hex-encoded maze is written
- `SEED` (optional): integer seed for deterministic generation

> Coordinate convention used by the project: `x` is the column index, `y` is the row index.

---

## Hexadecimal export format

The maze is exported as a rectangular grid of hex digits (`0`–`F`), one text line per row.

Each hex character encodes a **4-bit value** describing the walls of a cell.
Adjacent cells must agree on shared walls.

A provided script can validate the encoding consistency:

```bash
python3 output_validator.py <output_file>
```

---

## Maze generation algorithm

### Chosen algorithm

This project uses **Depth-First Search (DFS)**  for generation:

1. Start from a cell
2. Choose a random unvisited neighbor
3. Remove the wall between the current cell and the neighbor
4. Move to the neighbor
5. If there are no unvisited neighbors, backtrack
6. Continue until all cells are visited

### Why this algorithm

We chose DFS/backtracking because:
- It is straightforward to implement and debug
- It runs fast for typical maze sizes
- It naturally generates “long corridor” mazes that look good in terminal rendering
- It is a classic reference algorithm, widely documented and easy to explain in an academic setting

---

## Reusable code

The reusable part of the project is the **`mazegen`** package.

It is designed to be imported from other Python programs to:
- Create a grid representation of a maze
- Generate a maze (using the selected algorithm)
- Solve the maze and return a path
- Print/render the maze in terminal
- Export the maze in hexadecimal format

### Minimal example

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=10,
    height=10,
    seed=100,
    perfect=True,
    start=(0, 0),
    end=(9, 9),
    output_file="output_maze.txt",
    fixed_seed_flag=True,
)

grid = gen.create_grid()
gen.generate_maze(grid)
path = gen.solve_maze(grid, False)
gen.print_maze(grid, gen.start, gen.end, path, "\033[92m")
```

---

## Team and project management

### Team members and roles

- `aaliali` — (edit me: generation algorithm, solver, grid model, etc.)

- `yobouaji` — (edit me: describe exactly what you did, e.g., config parsing, UI/menu, rendering, export, packaging)
### Planning (and how it evolved)

Initial plan:
- (edit me) Example: “Day 1: grid + walls model; Day 2: DFS generation; Day 3: solver; Day 4: export + validation; Day 5: packaging + cleanup. etc... days”


### What worked well

- Separation between the CLI script (`a_maze_ing.py`) and the reusable library (`mazegen`)
- Deterministic generation via seed (useful for debugging and evaluation)
- Validator script to verify hex encoding

### What could be improved

- Add automated tests (unit tests for parsing, encoding, solver correctness)
- Support multiple generation algorithms (Prim, Kruskal, Wilson, etc.)
- Improve terminal UI (optional animation, better colors, resize handling)

### Tools used

- Python 3.10+
- Git / GitHub
- (Optional) Makefile
- `flake8` and `mypy` for linting/type checks
- `pdb` for debugging

---

## Resources

### Maze generation / theory

- Wikipedia — Maze generation algorithms
- Jamis Buck — *Mazes for Programmers* (excellent practical explanations)
- DFS / recursive backtracking references (articles + tutorials)

### Python / terminal rendering

- Python `colorama` documentation (ANSI colors on Windows)


### AI usage (what, where, how)

AI tools were used as a learning aid for:
- Reviewing README structure to match the 42 requirements
- Improving documentation clarity (sections, wording)
- Double-checking the standard explanation of DFS backtracking

AI tools were **not** used to automatically generate the full project source code.


---

    - aaliali and yobouaji thank you for your understanding and your kind treatment