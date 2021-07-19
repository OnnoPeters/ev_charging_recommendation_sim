from helper_files.simulation_parameters import NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR
from .rc_simulation_base import RecommendationCenter
import random


class RCSmallestAmountOfTimeLost(RecommendationCenter):
    def recommend_charging_station(self, car):
        selected_charging_station = None
        selected_charging_station_arrival_time = None
        selected_charging_station_leaving_time = None
        selected_charging_station_time_lost = None
        selected_charging_station_fast_charge = None

        for charging_station in self.charging_stations:
            if car.car_number == 1:
                print("SAOTL FREE ", charging_station.charging_station_number, charging_station.get_number_of_free_spots(), charging_station.charging_spots.count, charging_station.get_queue_size())
            x, y = charging_station.get_location()
            one_way_distance = car.calculate_distance(x, y)
            two_way_distance = one_way_distance + (abs(car.destination[0] - x) + abs(car.destination[1] - y))
            distance_to_destination = abs(car.destination[0] - car.x_coordinate) + abs(car.destination[1] - car.y_coordinate)
            current_occupation = self.get_cs_occupation(charging_station.charging_station_number, self.env.now + one_way_distance)
            current_fast_spot_occupation = self.get_fast_spot_occupation(charging_station.charging_station_number, self.env.now + one_way_distance)

            fast_charge = False
            if current_occupation >= self.capacity:
                occupation_list = self.get_cs_arrival_and_departure_list(charging_station.charging_station_number, self.env.now + one_way_distance)
                fast_spot_occupation_list = self.get_fast_spots_arrival_and_departure_list(charging_station.charging_station_number, self.env.now + one_way_distance)
                charging_start = occupation_list[-(self.capacity)]
                waiting_time = (self.env.now + one_way_distance) - charging_start
                if charging_start in fast_spot_occupation_list:
                    fast_charge = True
            else:
                waiting_time = 0
                if current_fast_spot_occupation < self.number_of_fast_chargers:
                    fast_charge = True

            if fast_charge:
                charging_time = int((1000000 - car.energy_units + one_way_distance) * FAST_CHARGING_FACTOR)
            else:
                charging_time = int((1000000 - car.energy_units + one_way_distance) * NORMAL_CHARGING_FACTOR)

            arrival_time = one_way_distance + self.env.now
            leaving_time = arrival_time + waiting_time + charging_time
            time_lost = (two_way_distance + waiting_time + charging_time) - distance_to_destination

            if car.car_number == 1:
                print(charging_station.charging_station_number, two_way_distance, arrival_time, waiting_time, charging_time, time_lost)
            if selected_charging_station is None or time_lost < selected_charging_station_time_lost:
                selected_charging_station = charging_station
                selected_charging_station_arrival_time = arrival_time
                selected_charging_station_leaving_time = leaving_time
                selected_charging_station_time_lost = time_lost
                selected_charging_station_fast_charge = fast_charge

        nearest_charging_station = None
        nearest_charging_station_distance = None

        for charging_station in self.charging_stations:
            nearest_x, nearest_y = charging_station.get_location()
            distance = car.calculate_distance(nearest_x, nearest_y) + (
                    abs(car.destination[0] - nearest_x) + abs(car.destination[1] - nearest_y))
            if nearest_charging_station is None or distance < nearest_charging_station_distance:
                nearest_charging_station = charging_station
                nearest_charging_station_distance = distance

        if selected_charging_station != nearest_charging_station:
            if random.randint(0, 100) > car.acceptance * 100:
                selected_charging_station = nearest_charging_station
                car.nearest = True
            else:
                car.nearest = False

        if not car.nearest:
            self.future_cs_arrivals[selected_charging_station.charging_station_number].append(selected_charging_station_arrival_time)
            #self.future_cs_departures[selected_charging_station.charging_station_number].append(selected_charging_station_leaving_time)
            self.cars_arriving_list[selected_charging_station.charging_station_number].append(car.car_number)
            if selected_charging_station_fast_charge:
                self.future_fast_spots_arrivals[selected_charging_station.charging_station_number].append(selected_charging_station_arrival_time)
                #self.future_fast_spots_departures[selected_charging_station.charging_station_number].append(selected_charging_station_leaving_time)
                self.cars_arriving_fast_spots_list[selected_charging_station.charging_station_number].append(car.car_number)

        if car.car_number == 1:
            print("Car 1 predictions:")
            print(self.env.now)
            print(selected_charging_station_arrival_time)
            print(selected_charging_station_leaving_time)
            print(selected_charging_station_time_lost)
            print("Fast:", selected_charging_station_fast_charge, self.get_fast_spot_occupation(selected_charging_station.charging_station_number, self.env.now))
        if car.car_number == 1:
            print("NEAREST ", nearest_charging_station.charging_station_number)
            print("CHOOSE ", selected_charging_station.charging_station_number)

        return selected_charging_station
