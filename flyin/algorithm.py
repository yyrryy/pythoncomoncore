import heapq
from typing import Optional

class Path_finder:
    """Dijkstra pathfinding on the parsed zone graph."""

    def __init__(self, zones: list[dict], connections: list[dict]) -> None:
        """Initialize with the list of zone dicts from the parser.

        Args:
            zones: List of zone dictionaries from Data.get_dict()
        """
        self.zones: dict[str, dict] = {zone["name"]: zone for zone in zones}
        self.connections: dict[str, dict] = connections

    def find_path(self, start: str, end: str) -> Optional[list[str]]:
        costs = {name: float("inf") for name in self.zones}
        costs[start] = 0
        previous = {name: None for name in self.zones}
        visited = set()
        # (cost, is_priority, zone_name) - is_priority=0 means priority zone (higher priority in heap)
        heap = [(0, 1, start)]  # lower is_priority = better (0 for priority, 1 for normal)

        while heap:
            current_cost, current_priority_flag, current_name = heapq.heappop(heap)

            if current_name in visited:
                continue
            visited.add(current_name)

            if current_name == end:
                return self.build_path(previous, start, end)

            for neighbor_name in self.zones[current_name]["connected_to"]:
                if neighbor_name in visited:
                    continue
                neighbor = self.zones[neighbor_name]
                if neighbor["zone_type"] == "blocked":
                    continue
                new_cost = current_cost + neighbor["cost"]
                if new_cost < costs[neighbor_name]:
                    costs[neighbor_name] = new_cost
                    previous[neighbor_name] = current_name
                    # Priority flag: 0 for priority zones (higher priority), 1 for normal
                    priority_flag = 0 if neighbor["zone_type"] == "priority" else 1
                    heapq.heappush(heap, (new_cost, priority_flag, neighbor_name))
                elif new_cost == costs[neighbor_name]:
                    # Same cost - prefer priority zones
                    existing_is_priority = (self.zones[neighbor_name]["zone_type"] == "priority")
                    new_is_priority = (neighbor["zone_type"] == "priority")
                    if new_is_priority and not existing_is_priority:
                        costs[neighbor_name] = new_cost
                        previous[neighbor_name] = current_name
                        priority_flag = 0 if neighbor["zone_type"] == "priority" else 1
                        heapq.heappush(heap, (new_cost, priority_flag, neighbor_name))

        return None

    def build_path(
        self,
        previous: dict[str, Optional[str]],
        start: str,
        end: str
    ) -> list[str]:
        
        """Reconstruct path from previous dict.

        Args:
            previous: Dict mapping each zone to the zone it was reached from.
            start: Start zone name.
            end: End zone name.

        Returns:
            Ordered list of zone names from start to end.
        """
        path: list[str] = []
        current: Optional[str] = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path

    def find_all_paths(self, start: str, end: str, paths_needed: int) -> list[list[str]]:
        """Find all simple paths from start to end using DFS.

        Args:
            start: Start zone name.
            end: End zone name.

        Returns:
            List of paths, each path is a list of zone names, sorted by cost.
        """
        all_paths: list[list[str]] = []
        self._dfs(start, end, [start], set([start]), all_paths, paths_needed)
        all_paths.sort(key=lambda p: self._path_cost(p))
        return all_paths

    def _dfs(
        self,
        current: str,
        end: str,
        path: list[str],
        visited: set[str],
        all_paths: list[list[str]],
        paths_needed: int
    ) -> None:
        """Recursive DFS to find all simple paths.

        Args:
            current: Current zone name.
            end: Target zone name.
            path: Current path being explored.
            visited: Set of visited zone names in current path.
            all_paths: Accumulator for completed paths.
        """
        
        if current == end:
            all_paths.append(list(path))
            return
        for neighbor_name in self.zones[current]["connected_to"]:
            if len(all_paths) > paths_needed:
                break
            if neighbor_name in visited:
                continue
            neighbor = self.zones[neighbor_name]
            if neighbor["zone_type"] == "blocked":
                continue
            print(neighbor)
            try:
                connection = next(i for i in self.connections if i['from']==current and i['to']==neighbor_name)
                print(f"connection {current} {neighbor_name} {connection['max_link_capacity']}")
                path.append(f"{neighbor_name}:{connection['max_link_capacity']}:{neighbor['max_drones']}")
            except Exception:
                path.append(f"{neighbor_name}:0:0")
            visited.add(neighbor_name)
            self._dfs(neighbor_name, end, path, visited, all_paths, paths_needed)
            path.pop()
            visited.remove(neighbor_name)

    def _path_cost(self, path: list[str]) -> int:
        """Calculate total cost of a path.

        Args:
            path: List of zone names.

        Returns:
            Total turn cost of the path.
        """
        s = 0
        for i in path[1:]:
            zone_name = i.split(":")[0]
            s += self.zones[zone_name]["cost"]
        return s
