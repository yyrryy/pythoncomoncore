import re

class Parsing_error(Exception):
    ...


# each zone may have color=None zone_type="normal", max_drones=1, cost=1
class Zone():
    def __init__(
        self,
        name: str,
        is_start: bool,
        is_end: bool,
        x: int,
        y: int,
        attributes: str,
    ) -> None:
        self.name = name
        self.is_start = is_start
        self.is_end = is_end
        self.x = x
        self.y = y
        self.attributes = attributes
        self.zone_type = "normal"
        self.color = None
        self.cost = 1
        self.max_drones = 1
        self.connected_to = []
        self.data = {
            "name": self.name,
            "cost": self.cost,
            "x": self.x,
            "y": self.y,
            "connected_to": self.connected_to
        }

    def get_data(self, l_dx):
        if self.attributes:

            splitted = (self.attributes).split()
            for i in splitted:
                attr_pattern = re.compile(r'^([a-z_]+)=([^=\s]+)$')
                valid_attribute = attr_pattern.match(i)
                if not valid_attribute:
                    raise Parsing_error(f"Not a valid attribute, line {l_dx}")
                key, val = valid_attribute.group(1), valid_attribute.group(2)
                if key == "color":
                    self.color = val

                elif key == "zone":
                    self.zone_type = val
                    if val == "restricted":
                        self.cost = 2
                    elif val == "blocked":
                        self.cost = 0
                elif key == "max_drones":
                    try:
                        self.max_drones = int(val)
                    except ValueError:
                        raise Parsing_error(f"{val} is not a valid number, line: {l_dx}")
                
        else:
            self.color = None
            self.zone_type = "normal"
            self.max_drones = 1

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "is_start": self.is_start,
            "is_end": self.is_end,
            "x": self.x,
            "y": self.y,
            "zone_type": self.zone_type,
            "color": self.color,
            "max_drones": self.max_drones,
            "cost": self.cost,
            "connected_to": [z.name for z in self.connected_to],
        }
    

class Conncetion():
    def __init__(self, zone_from: Zone, zone_to: Zone, attributes: dict):
        self.zone_from = zone_from
        self.zone_to = zone_to
        self.attributes = attributes
        self.data = {}


class Data():
    def __init__(self,
                 nb_drones: int, start: tuple, end: tuple,
                 zones: list[Zone], connections: list[Conncetion]):
        self.nb_drones = nb_drones
        self.start = start
        self.end = end
        self.zones = zones
        self.connections = connections

    def get_dict(self) -> dict:
        return {
            "nb_drones": self.nb_drones,
            "zones": [i.get_dict() for i in self.zones],
        }

    def parse_data(self, file_content):
        # #if True then it has already parsed else not parsed
        start_flag = False
        end_flag = False
        # l_dx = line index
        for l_dx, line in enumerate(file_content):
            if line.startswith("#"):
                continue
            l_dx += 1
            # start hub pattern
            # the start flag to  catch the start hub parsing
            nb_drones_pattern = r'^nb_drones:\s+([\d.]+)?'
            start_hub_pattern = r'^start_hub:\s+([\w-]+)\s+([\d.]+)\s+([\d.]+)(?:\s+\[([^\]]*)\])?'
            end_hub_pattern = r'^end_hub:\s+([\w-]+)\s+([\d.]+)\s+([\d.]+)(?:\s+\[([^\]]*)\])?'
            hub_pattern = r'^hub:\s+([\w-]+)\s+([\d.]+)\s+([\d.]+)(?:\s+\[([^\]]*)\])?'
            connection_pattern = r'^connection:\s+([\w-]+)(?:\s+\[([^\]]*)\])?'
            nb_drones_match = re.match(nb_drones_pattern, line)
            start = re.match(start_hub_pattern, line)
            end = re.match(end_hub_pattern, line)
            hub = re.match(hub_pattern, line)
            connection = re.match(connection_pattern, line)
            # enforce the first line to be the number of drones
            if l_dx == 1 and not nb_drones_match:
                raise Parsing_error("the first line should be the number of drones")
            if nb_drones_match:
                number = int(nb_drones_match.group(1))
                self.nb_drones = number
            if start:
                name = start.group(1)
                if "-" in name or " " in name:
                    raise Parsing_error(f"Zone name cannot contain dashes or spaces, line: {l_dx}")
                if start_flag:
                    message = f"{name} already existed, Error in line {l_dx}"
                    raise Parsing_error(message)
                start_flag = True
                x = int(start.group(2))
                y = int(start.group(3))
                attributes = start.group(4)
                zone = Zone(name, True, False, x, y, attributes)
                zone.get_data(l_dx)
                self.zones.append(zone)
                self.start = (x, y)
            if end:
                name = end.group(1)
                if "-" in name or " " in name:
                    raise Parsing_error(f"Zone name cannot contain dashes or spaces, line: {l_dx}")
                if end_flag:
                    message = f"{name} already existed, Error in line {l_dx}"
                    raise Parsing_error(message)
                end_flag = True
                x = int(end.group(2))
                y = int(end.group(3))
                attributes = end.group(4)
                zone = Zone(name, False, True, x, y, attributes)
                zone.get_data(l_dx)
                self.zones.append(zone)
                self.end = (x, y)
            if hub:
                name = hub.group(1)
                if "-" in name or " " in name:
                    raise Parsing_error(f"Zone name cannot contain dashes or spaces, line: {l_dx}")
                x = int(hub.group(2))
                y = int(hub.group(3))
                attributes = hub.group(4)
                print("name from hub", name, x, y, attributes)
                zone = Zone(name, False, False, x, y, attributes)
                zone.get_data(l_dx)
                self.zones.append(zone)
            if connection:
                zones = connection.group(1)
                splitted = zones.split("-")
                if len(splitted) > 2:
                    raise Parsing_error(f"Not valid connection, line: {l_dx}")
                zone_from = splitted[0]
                zone_to = splitted[1]
                attributes = connection.group(2)
                cretaed_connections = self.create_connection(
                    zone_from,
                    zone_to,
                    attributes,
                    l_dx
                )
                self.connections.append(cretaed_connections)
        if not start_flag:
            raise Parsing_error("start hub does not exist")
        if not end_flag:
            raise Parsing_error("end hub does not exist")

    def create_connection(
        self,
        zone_from: str,
        zone_to: str,
        attributes: str,
        l_dx
    ) -> Conncetion:
        print(zone_from, zone_to)
        zone_from_instence = next((z for z in self.zones if z.name == zone_from), None)
        if not zone_from_instence:
            message = f"Zone {zone_from} does not exist, line {l_dx}"
            raise Parsing_error(message)
        # if there is zone from the proceed with the remain logic
        zone_to_instence = next((z for z in self.zones if z.name == zone_to), None)
        if not zone_to_instence:
            message = f"Zone {zone_to} does not exist, line {l_dx}"
            raise Parsing_error(message)
        # else means there is zone from and zone to
        else:
            zone_from_instence.connected_to.append(zone_to_instence)
            connection_instence = Conncetion(zone_from, zone_to, attributes)
            # connection_instence.data[""]
            if attributes:
                try:
                    max_link = int(attributes.split("max_link_capacity=")[1])
                    connection_instence.data["max_link_capacity"] = max_link
                except ValueError:
                    message = f"Not valid max_link_capacity ({max_link}), "
                    message += f"line: {l_dx}"
                    raise Parsing_error(message)
            # else, means no attributes providedm do the defaults:
            else:
                connection_instence.data["max_link_capacity"] = 1
            return connection_instence

