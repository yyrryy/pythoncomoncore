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
        self.drones_in_connection = {(c["from"], c["to"]): [] for c in connections}

    def create_drones(self) -> list[Drone]:
        drones = [Drone(i + 1, self.start_zone) for i in range(self.nb_drones)]
        self.drones = drones
        self.drones_in_zone[self.start_zone] = [d.id for d in drones]
    def assign_paths(self) -> None:
        for i in self.drones:
            pathfinder =  Path_finder(self.zones, self.connections)
            #this will assign same path for all
            #i.path = pathfinder.find_path(start_zone, end_zone)
            all_paths = pathfinder.find_all_paths(self.start_zone, self.end_zone, paths_needed=self.nb_drones)
            if len(all_paths) == 0:
                raise ValueError("No path found in this graph")
            for i, drone in enumerate(self.drones):
                path_index = i % len(all_paths)  # ← round-robin
                full_path = all_paths[path_index]
                drone.path = full_path[1:] if len(full_path) > 1 else []
    def run(self) -> None:
        self.create_drones()
        self.assign_paths()
        # for i in self.drones:
        #     # with open("drones.txt", "a") as f:
        #     #     print(f"{i.id}: {'-'.join(str(i) for i in i.path)}", file=f)
        while not all(drone.status == DroneStatus.DELIVERED for drone in self.drones):
            self.turn += 1
            self.process_turn()  # ← you'll write this

    def process_turn(self) -> None:
        movements_this_turn = []  # List of (drone, destination) strings
        for drone in self.drones:
            if drone.status == DroneStatus.DELIVERED:
                continue
            current_zone = drone.current_zone
            next_zone = drone.path[0] if drone.path else None
            # print(f">>>>>>>>> D{drone.id} can move from {current_zone} to {next_zone}", self.can_move(drone, current_zone, next_zone))
            if next_zone and self.can_move(drone, current_zone, next_zone):
                # gt connection to know max_link_capacity
                
                movements_this_turn.append(self.move_drone(drone, current_zone, next_zone))
        print(*movements_this_turn)
        # movements_this_turn = []  # List of (drone, destination) strings
    
        # for drone in self.drones:
        #     if drone.status == DroneStatus.DELIVERED:
        #         continue
        #     current_zone = drone.current_zone
        #     # Handle flying drones (arrivals already done)
        #     if drone.status == DroneStatus.MOVING:
        #         continue
            
        #     # Waiting drone - check if it can move
        #     if drone.path:
        #         next_zone = drone.path[0]
        #         if next_zone and self.can_move(drone, current_zone, next_zone):
        #             # Execute the move
        #             self.move_drone(drone, current_zone, next_zone)
                    
        #             # Add to output for this turn
        #             movements_this_turn.append(f"D{drone.id}-{next_zone}")
        
        # # Step 3: Print all movements for this turn
        # if movements_this_turn:
        #     print(" ".join(movements_this_turn))
        #     # Also save to file if needed

    def can_move(self, drone: Drone, from_zone: str, to_zone: str) -> bool:
        # Check if drone can move from from_zone to to_zone
        # This is where you check for capacity, connections, etc.
        connection = next((c for c in self.connections if (c["from"] == from_zone and c["to"] == to_zone)), None)
        max_capacity = connection["max_link_capacity"]
        to_zone_instence = next(z for z in self.zones if z["name"] == to_zone)
        max_drones_in_zone = to_zone_instence["max_drones"]
        drones_in_zone = len(self.drones_in_zone[to_zone])
        drones_in_connection = len(self.drones_in_connection[(from_zone, to_zone)])
        can_move = True
        # ila kan moving means kan *'adi lrestricted w w9ef fnes tri9
        if drone.status == DroneStatus.MOVING:
            if drone.id in self.drones_in_connection[(from_zone, to_zone)]:
                # check if it can enter the zone_to
                return True
        if drones_in_zone >= max_drones_in_zone or drones_in_connection >= max_capacity:
            drone.status = DroneStatus.MOVING
            return False
        if to_zone_instence["zone_type"] == "restricted":
            if drone.id in self.drones_in_connection[(from_zone, to_zone)]:
                if  drones_in_connection < max_capacity:
                    self.drones_in_connection[(from_zone, to_zone)].append(drone.id)
                    drone.status = DroneStatus.MOVING
                    return False
            
        # print(f"Turn {self.turn}: Checking if Drone {drone.id} can move from {from_zone} to {to_zone} - Drones in zone: {drones_in_zone}/{max_drones_in_zone}, Drones in connection: {drones_in_connection}/{max_capacity} - Can move: {can_move}")
        # if to_zone_state["zone_type"] == "restricted":
        #     # drone.status = DroneStatus.MOVING
        #     if drone.id in self.drones_in_connection[(from_zone, to_zone)]:
        #         self.drones_in_connection[(from_zone, to_zone)].remove(drone.id)
        #         return True
        #     if len(self.drones_in_connection[(from_zone, to_zone)]) >= max_capacity:
        #         drone.status = DroneStatus.WAITING
        #         return False
        #     self.drones_in_connection[(from_zone, to_zone)].append(drone.id)
        # # if len(self.drones_in_zone[to_zone]) + len(to_zone_state.get("incoming_drones", [])) >= to_zone_state["max_drones"]:
        # #     return False
        # if len(self.drones_in_zone[to_zone]) >= to_zone_state["max_drones"]:
        #     return False
        return True
        return can_move
    def move_drone(self, drone: Drone, from_zone: str, to_zone: str) -> str:
        # Move drone and update status
        drone.current_zone = to_zone
        drone.path.pop(0)
        self.drones_in_zone[from_zone].remove(drone.id)
        self.drones_in_zone[to_zone].append(drone.id)
        if drone.id in self.drones_in_connection[(from_zone, to_zone)]:
            self.drones_in_connection[(from_zone, to_zone)].remove(drone.id)
        # with open("movements.txt", "a") as f:
        if to_zone == self.end_zone:
            drone.status = DroneStatus.DELIVERED
        return f"D{drone.id}-{to_zone}"