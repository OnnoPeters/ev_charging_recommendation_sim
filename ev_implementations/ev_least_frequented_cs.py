import random

from ev_implementations.ev_simulation_base import BaseEV


class EVLeastFrequented(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None
        selected_charging_station_queue_size = None
        selected_charging_station_cars = None
        found_free_spot = False

        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("FCASQ FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            cars_currently = charging_station.get_number_of_cars()

            if selected_charging_station is None or cars_currently < selected_charging_station_cars or (selected_charging_station_cars == cars_currently and distance < selected_charging_station_distance):
                selected_charging_station = charging_station
                selected_charging_station_distance = distance
                selected_charging_station_cars = cars_currently

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

        if self.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        self.charging_station_destination = selected_charging_station


