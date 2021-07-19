from ev_implementations.ev_simulation_base import BaseEV
import random


class EVRandomCS(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = random.choice(self.charging_stations)

        nearest_charging_station = None
        nearest_charging_station_distance = None

        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = self.calculate_distance(nearest_x, nearest_y) + (abs(self.destination[0] - nearest_x) + abs(self.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        if selected_charging_station != nearest_charging_station:
            if random.randint(0, 100) > self.acceptance * 100:
                selected_charging_station = nearest_charging_station

        self.charging_station_destination = selected_charging_station
