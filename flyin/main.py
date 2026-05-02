# main.py
import sys
from parser import Parser
from exceptions import Parsing_error
from algorithm import Path_finder
from simulation import Simulation
def main(filepath: str, verbose: bool = True) -> None:
    """Main entry point."""
    try:
        with open(filepath) as file:
            file_content = file.readlines()

        parser = Parser()
        parser.parse_data(file_content)
        data = parser.get_dict()
        # Run simulation with verbose output
        pathfinder = Path_finder(data["zones"], data["connections"])
        start_zone = next(i["name"] for i in data["zones"] if i["is_start"])
        end_zone = next(i["name"] for i in data["zones"] if i["is_end"])
        sim = Simulation(data["nb_drones"], data["zones"], data["connections"], start_zone, end_zone)
        sim.run()
        # paths_needed = round((data["nb_drones"])/2)
        # with open("t.txt", "w") as f:
        #     print(data["zones"], file=f)
        # allpaths = pathfinder.find_all_paths(start_zone, end_zone, paths_needed)
        # with open("connections.txt", "w") as f:
        #     print(data['connections'], file=f)
        # with open("paths.txt", "w") as f:
        #     print(allpaths, file=f)
    except Parsing_error as e:
        print(f"Parse Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found", file=sys.stderr)
        sys.exit(1)
        # todo: uncomment this
    # except Exception as e:
    #     print("Unexpected error", e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <map_file> [--quiet]", file=sys.stderr)
        sys.exit(1)
    
    verbose = "--quiet" not in sys.argv
    map_file = sys.argv[1]
    
    main(map_file, verbose=verbose)