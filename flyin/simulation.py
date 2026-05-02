from classes import Drone, DroneStatus
from algorithm import Path_finder

class Simulation():
    def __init__(self, nb_drones: int, zones: list[dict], connections: list[dict], start_zone: str, end_zone: str):
        self.nb_drones = nb_drones
        self.zones = zones
        self.connections = connections
        self.start_zone = start_zone
        self.end_zone = end_zone
        self.drones = []           # ← will hold drones
        self.turn = 0              # ← track current turn
        self.drones_in_zone = {z["name"]: [] for z in zones}

    def create_drones(self) -> list[Drone]:
        drones = [Drone(i + 1, self.start_zone, self.end_zone) for i in range(self.nb_drones)]
        self.drones = drones
        self.drones_in_zone[self.start_zone] = [d.id for d in drones]
    def assign_paths(self) -> None:
        for i in self.drones:
            pathfinder =  Path_finder(self.zones, self.connections)
            #this will assign same path for all
            #i.path = pathfinder.find_path(start_zone, end_zone)
            all_paths = pathfinder.find_all_paths(self.start_zone, self.end_zone, paths_needed=self.nb_drones)
            for i, drone in enumerate(self.drones):
                path_index = i % len(all_paths)  # ← round-robin
                full_path = all_paths[path_index]
                drone.path = full_path[1:] if len(full_path) > 1 else []
    def run(self) -> None:
        self.create_drones()
        self.assign_paths()
        for i in self.drones:
            with open("drones.txt", "a") as f:
                print(f"{i.id}: {'-'.join(str(i) for i in i.path)}", file=f)
        # while not all(drone.status == "delivered" for drone in self.drones):
        #     self.turn += 1
        #     self.process_turn()  # ← you'll write this

    def process_turn(self) -> None:
        # This will handle one turn of movement
        pass