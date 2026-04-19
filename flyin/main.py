from parser import Data, Parsing_error
from djikstra import Dijkstra

with open("test.txt") as file:
    file_content = file.readlines()
init = Data(0, (), (), [], [])
try:
    init.parse_data(file_content)
    data = init.get_dict()
    dijkstra = Dijkstra(data["zones"])
    print(data)
    # single best path
    start_name = next(z["name"] for z in data["zones"] if z["is_start"])
    end_name = next(z["name"] for z in data["zones"] if z["is_end"])
    best = dijkstra.find_path(start_name, end_name)

    # all valid paths sorted by cost
    all_paths = dijkstra.find_all_paths(start_name, end_name)
    print(best)
except Parsing_error as e:
    print(e)

