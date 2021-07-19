from ev_implementations.ev_simulation_base import BaseEV


class EVNearestCS(BaseEV):
    def set_charging_station_as_destination(self):
        selected_charging_station = None
        selected_charging_station_distance = None

        for charging_station in self.charging_stations:
            if self.car_number == 1:
                print("NEAREST FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.get_queue_size())
            x, y = charging_station.get_location()
            distance = self.calculate_distance(x, y) + (abs(self.destination[0] - x) + abs(self.destination[1] - y))
            if selected_charging_station is None or distance < selected_charging_station_distance:
                selected_charging_station = charging_station
                selected_charging_station_distance = distance

        if self.car_number == 1:
            print("CHOOSE ", selected_charging_station.charging_station_number)



        self.charging_station_destination = selected_charging_station




