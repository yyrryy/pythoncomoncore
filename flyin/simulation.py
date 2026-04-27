# simulation.py
from typing import Optional
from collections import defaultdict
from classes import Drone, ZoneState, ConnectionState, DroneStatus
from algorithm import Dijkstra_algo
import sys


class Simulation:
    """Main simulation engine for multi-drone routing."""

    def __init__(self, data: dict, verbose: bool = True):
        self.nb_drones = data["nb_drones"]
        self.zones_data = {z["name"]: z for z in data["zones"]}
        self.connections_data = data["connections"]
        self.verbose = verbose  # Enable/disable terminal output

        # Find start and end zones
        self.start_zone = next(z["name"] for z in data["zones"] if z["is_start"])
        self.end_zone = next(z["name"] for z in data["zones"] if z["is_end"])

        # Initialize pathfinder
        self.pathfinder = Dijkstra_algo(data["zones"])

        # Precompute all paths for each drone (will be assigned dynamically)
        self.all_paths = self.pathfinder.find_all_paths(self.start_zone, self.end_zone)

        # Dynamic state
        self.zones_state: dict[str, ZoneState] = {}
        self.connections_state: dict[tuple[str, str], ConnectionState] = {}
        self.drones: list[Drone] = []

        self._init_states()
        self._init_drones()

        self.turn = 0
        self.movements_log: list[str] = []

        # Print initial setup
        if self.verbose:
            self._print_header()

    def _print_header(self) -> None:
        """Print simulation header information."""
        print("\n" + "=" * 60, file=sys.stderr)
        print("🚁 DRONE SIMULATION STARTING", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"📊 Total Drones: {self.nb_drones}", file=sys.stderr)
        print(f"📍 Start Zone: {self.start_zone}", file=sys.stderr)
        print(f"🎯 End Zone: {self.end_zone}", file=sys.stderr)
        print(f"🗺️  Total Zones: {len(self.zones_data)}", file=sys.stderr)
        print(f"🔗 Total Connections: {len(self.connections_data)}", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print("\n📋 Movement Log:", file=sys.stderr)
        print("-" * 40, file=sys.stderr)

    def _print_turn_start(self) -> None:
        """Print turn start information."""
        delivered = sum(1 for d in self.drones if d.current_zone == self.end_zone)
        in_transit = sum(1 for d in self.drones if d.status == DroneStatus.MOVING)
        waiting = sum(1 for d in self.drones if d.status == DroneStatus.WAITING and d.current_zone != self.end_zone)
        
        print(f"\n🔄 Turn {self.turn} | Delivered: {delivered}/{self.nb_drones} | "
              f"Moving: {in_transit} | Waiting: {waiting}", file=sys.stderr)

    def _print_movements(self, movements: list[str]) -> None:
        """Print movements for current turn."""
        if movements:
            print(f"   ✈️  {', '.join(movements)}", file=sys.stderr)
        else:
            print("   ⏸️  No movements this turn", file=sys.stderr)

    def _print_zone_status(self) -> None:
        """Print current zone occupancy status (for debugging)."""
        if not self.verbose:
            return
        
        occupied_zones = {
            name: state.current_drones 
            for name, state in self.zones_state.items() 
            if state.current_drones
        }
        
        if occupied_zones:
            print("   📍 Zone occupancy:", file=sys.stderr)
            for zone, drones in list(occupied_zones.items())[:5]:  # Limit to 5 zones
                drone_str = f"D{', D'.join(map(str, drones))}" if drones else "empty"
                print(f"      {zone}: [{drone_str}]", file=sys.stderr)

    def _print_summary(self) -> None:
        """Print final simulation summary."""
        print("\n" + "=" * 60, file=sys.stderr)
        print("✅ SIMULATION COMPLETE", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        print(f"📊 Total Turns: {self.turn}", file=sys.stderr)
        print(f"🚁 Drones Delivered: {self.nb_drones}/{self.nb_drones}", file=sys.stderr)
        
        # Calculate efficiency metrics
        if self.movements_log:
            total_moves = sum(len(log.split()) for log in self.movements_log)
            avg_moves_per_turn = total_moves / self.turn if self.turn > 0 else 0
            print(f"📈 Average Moves Per Turn: {avg_moves_per_turn:.2f}", file=sys.stderr)
            print(f"🔄 Total Movements: {total_moves}", file=sys.stderr)
        
        print("=" * 60, file=sys.stderr)

    def _init_states(self) -> None:
        """Initialize zone and connection states."""
        for name, data in self.zones_data.items():
            self.zones_state[name] = ZoneState(data)

        for conn in self.connections_data:
            key = (conn["from"], conn["to"])
            self.connections_state[key] = ConnectionState(
                conn["from"], conn["to"], conn["max_link_capacity"]
            )
            # Bidirectional
            rev_key = (conn["to"], conn["from"])
            self.connections_state[rev_key] = ConnectionState(
                conn["to"], conn["from"], conn["max_link_capacity"]
            )

    def _init_drones(self) -> None:
        """Create all drones at start zone."""
        for i in range(1, self.nb_drones + 1):
            drone = Drone(id=i, current_zone=self.start_zone)
            self.drones.append(drone)
        # Initialize start zone with all drones
        self.zones_state[self.start_zone].current_drones = list(range(1, self.nb_drones + 1))

    def _assign_path(self, drone: Drone) -> list[str]:
        """Assign a path to a drone based on current network state."""
        # TODO: Implement smarter path assignment considering congestion
        # For now, assign shortest path
        path = self.pathfinder.find_path(drone.current_zone, self.end_zone)
        if path:
            # Return path without current zone
            return path[1:] if len(path) > 1 else []
        return []

    def _can_move_to(
        self,
        drone: Drone,
        target_zone: str,
        connection_key: tuple[str, str]
    ) -> bool:
        """Check if drone can move to target zone this turn."""
        # Check zone capacity
        if not self.zones_state[target_zone].can_enter(drone.id):
            if self.verbose:
                print(f"      ⚠️  D{drone.id} cannot enter {target_zone} (capacity full)", file=sys.stderr)
            return False
        # Check connection capacity
        if not self.connections_state[connection_key].can_traverse(drone.id):
            if self.verbose:
                print(f"      ⚠️  D{drone.id} cannot use {connection_key[0]}→{connection_key[1]} (link full)", file=sys.stderr)
            return False
        # Check if target is not blocked
        if self.zones_data[target_zone]["zone_type"] == "blocked":
            if self.verbose:
                print(f"      ⚠️  D{drone.id} cannot enter {target_zone} (blocked zone)", file=sys.stderr)
            return False
        return True

    def _move_drone(
        self,
        drone: Drone,
        target_zone: str,
        connection_key: tuple[str, str]
    ) -> tuple[str, Optional[str]]:
        """
        Execute movement for a drone.
        Returns (movement_string, error_or_none)
        """
        dest_type = self.zones_data[target_zone]["zone_type"]

        # Reserve connection
        self.connections_state[connection_key].reserve(drone.id)

        if dest_type == "restricted":
            # Movement takes 2 turns
            drone.status = DroneStatus.MOVING
            drone.turns_remaining = 2
            drone.target_zone = target_zone
            drone.connection_name = f"{connection_key[0]}-{connection_key[1]}"
            if self.verbose:
                print(f"      🚁 D{drone.id} → {drone.connection_name} (restricted, 2 turns)", file=sys.stderr)
            return f"D{drone.id}-{drone.connection_name}", None
        else:
            # Normal or priority: 1 turn movement
            # Schedule arrival
            self.zones_state[target_zone].add_incoming(drone.id)
            # Remove from current zone
            self.zones_state[drone.current_zone].remove_drone(drone.id)
            drone.current_zone = target_zone
            zone_type_icon = "⭐" if dest_type == "priority" else "📍"
            if self.verbose:
                print(f"      ✈️  D{drone.id} → {target_zone} {zone_type_icon}", file=sys.stderr)
            return f"D{drone.id}-{target_zone}", None

    def _complete_multi_turn_moves(self) -> None:
        """Handle drones that are mid-flight through restricted zones."""
        for drone in self.drones:
            if drone.status == DroneStatus.MOVING and drone.turns_remaining > 0:
                drone.turns_remaining -= 1
                if self.verbose and drone.turns_remaining > 0:
                    print(f"      ⏳ D{drone.id} en route to {drone.target_zone} "
                          f"({drone.turns_remaining} turns remaining)", file=sys.stderr)
                if drone.turns_remaining == 0:
                    # Arrive at destination
                    drone.status = DroneStatus.WAITING
                    self.zones_state[drone.target_zone].add_incoming(drone.id)
                    self.zones_state[drone.current_zone].remove_drone(drone.id)
                    drone.current_zone = drone.target_zone
                    if self.verbose:
                        print(f"      🎯 D{drone.id} arrived at {drone.target_zone}", file=sys.stderr)
                    drone.target_zone = None

    def _process_arrivals_and_departures(self) -> None:
        """Commit all scheduled arrivals and connection reservations."""
        # Commit zone arrivals
        for zone_state in self.zones_state.values():
            zone_state.commit_arrivals()

        # Commit connection reservations
        for conn_state in self.connections_state.values():
            conn_state.commit_reservations()

    def _release_connections(self) -> None:
        """Release connections for drones that completed movement."""
        # For drones that arrived this turn, release the connection they used
        # This is handled by connection state management
        pass

    def step(self) -> list[str]:
        """Execute one simulation turn. Returns list of movements this turn."""
        previous_turn = self.turn
        self.turn += 1
        
        if self.verbose:
            self._print_turn_start()
        
        movements = []

        # First, complete any multi-turn moves
        self._complete_multi_turn_moves()

        # Determine which drones need to move
        drones_to_move = [
            d for d in self.drones
            if d.status == DroneStatus.WAITING
            and d.current_zone != self.end_zone
        ]

        # Assign paths to drones without one
        for drone in drones_to_move:
            if not drone.path:
                drone.path = self._assign_path(drone)
                if self.verbose and drone.path:
                    path_str = " → ".join([drone.current_zone] + drone.path)
                    print(f"      🗺️  D{drone.id} assigned path: {path_str}", file=sys.stderr)

        # Attempt to move each drone
        for drone in drones_to_move:
            if not drone.path:
                continue

            next_zone = drone.path[0]
            connection_key = (drone.current_zone, next_zone)

            if self._can_move_to(drone, next_zone, connection_key):
                movement_str, _ = self._move_drone(drone, next_zone, connection_key)
                movements.append(movement_str)
                # Remove from path after starting movement
                drone.path.pop(0)
            else:
                if self.verbose:
                    print(f"      ⏸️  D{drone.id} waiting at {drone.current_zone}", file=sys.stderr)

        # Print zone status after movements
        if self.verbose and movements:
            self._print_zone_status()

        # Commit all scheduled changes
        self._process_arrivals_and_departures()

        # Print movements summary
        if self.verbose:
            self._print_movements(movements)

        # Check for delivered drones
        newly_delivered = [
            d for d in self.drones 
            if d.current_zone == self.end_zone and d.status != DroneStatus.FINISHED
        ]
        for drone in newly_delivered:
            drone.status = DroneStatus.FINISHED
            if self.verbose:
                print(f"      🏆 D{drone.id} REACHED THE GOAL! 🏆", file=sys.stderr)

        return movements

    def run(self) -> list[str]:
        """Run simulation until all drones reach end zone."""
        all_movements = []

        while True:
            # Check if all drones finished
            finished = all(
                d.current_zone == self.end_zone or d.status == DroneStatus.FINISHED
                for d in self.drones
            )
            if finished:
                break

            movements = self.step()
            if movements:
                movement_line = " ".join(movements)
                all_movements.append(movement_line)
                self.movements_log.append(movement_line)

        if self.verbose:
            self._print_summary()

        return all_movements

    def get_summary(self) -> dict:
        """Get simulation summary statistics."""
        return {
            "total_turns": self.turn,
            "drones_delivered": sum(1 for d in self.drones if d.current_zone == self.end_zone),
            "total_drones": self.nb_drones,
            "movements_per_turn": [
                len(log.split()) for log in self.movements_log
            ] if self.movements_log else [],
        }