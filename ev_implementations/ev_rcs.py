from ev_implementations.ev_simulation_base import BaseEV
import random


class EVRCs(BaseEV):
    def __init__(self, env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor):
        super().__init__(env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor)
        self.rc = None
        self.nearest = False
        self.track_cs = False

    def get_recommendation_center(self, rc):
        """
        Sets the RC
        """
        self.rc = rc

    def set_charging_station_as_destination(self):
        """
        Makes the recommendation by the RC the charging station destination of this EV.
        """
        selected_charging_station = self.rc.recommend_charging_station(self)
        self.charging_station_destination = selected_charging_station

    def run(self):
        """
        The main flow of the EV in this simulation environment. Lets the EV drive to a CS first, after which it will drive to random destination and after that it will
        be off on a trip. If this EV is deactivated, the EV will do nothing here until it is reactivated.
        """
        while True:
            if not self.deactivated:
                self.generate_random_destination()
                self.set_charging_station_as_destination()

                direct_distance = self.calculate_distance(self.destination[0], self.destination[1])
                time_on_way_to_cs = self.calculate_distance(self.charging_station_destination.get_location()[0], self.charging_station_destination.get_location()[1]) + \
                                          (abs(self.destination[0] - self.charging_station_destination.get_location()[0]) + abs(self.destination[1] - self.charging_station_destination.get_location()[1])) - direct_distance

                self.time_on_way_to_cs += time_on_way_to_cs
                if self.car_number == 1:
                    print("DRIVING: ", self.env.now)
                self.number_of_chargings += 1

                yield self.drive_to_location()

                #Charging
                charging_spot = self.charging_station_destination.allocate_charging_spot()
                cs = self.charging_station_destination
                self.charging_station_destination = None
                #print("test", self.destination, self.x_coordinate, self.y_coordinate)
                if self.car_number == 1:
                    print("WAITING: ", self.env.now)

                waiting_start = self.env.now
                with charging_spot.request() as req:
                    yield req

                    waiting_end = self.env.now

                    waiting_time = waiting_end - waiting_start
                    if self.track_cs:
                        self.rc.add_waiting_time_to_cs(cs.charging_station_number, waiting_time)

                    #print(self.charging_station_destination)

                    if self.car_number == 1:
                        print("CHARGING: ", self.env.now)
                    is_fast_charging_spot = cs.check_free_fast_spot()
                    if is_fast_charging_spot:
                        charging_time = int((1000000 - self.energy_units) * self.fast_charging_factor)
                        leaving_time = self.env.now + int((1000000 - self.energy_units) * self.fast_charging_factor)
                        self.rc.future_cs_departures[cs.charging_station_number].append(leaving_time)
                        self.rc.future_fast_spots_departures[cs.charging_station_number].append(leaving_time)
                    else:
                        leaving_time = self.env.now + int((1000000 - self.energy_units) * self.normal_charging_factor)
                        self.rc.future_cs_departures[cs.charging_station_number].append(leaving_time)
                        charging_time = int((1000000 - self.energy_units) * self.normal_charging_factor)
                    self.charging_time += charging_time
                    if self.track_cs:
                        self.rc.add_charging_time_to_cs(cs.charging_station_number, charging_time)
                        self.rc.add_charging_to_cs(cs.charging_station_number)

                    yield self.start_charging(is_fast_charging_spot)
                    if is_fast_charging_spot:
                        cs.free_up_fast_spot()

                    #print("yo", self.env.now, car_index, self.car_number, self.rc.cars_arriving_list[cs.charging_station_number][car_index],self.rc.future_cs_arrivals[cs.charging_station_number][car_index])
                    if not self.nearest:
                        car_index = self.rc.cars_arriving_list[cs.charging_station_number].index(self.car_number)
                        departure_index = self.rc.future_cs_departures[cs.charging_station_number].index(leaving_time)

                        del self.rc.cars_arriving_list[cs.charging_station_number][car_index]
                        del self.rc.future_cs_arrivals[cs.charging_station_number][car_index]
                        del self.rc.future_cs_departures[cs.charging_station_number][departure_index]
                        if is_fast_charging_spot:
                            if self.car_number in self.rc.cars_arriving_fast_spots_list[cs.charging_station_number]:
                                fast_spot_car_index = self.rc.cars_arriving_fast_spots_list[cs.charging_station_number].index(self.car_number)
                                fast_spot_departure_index = self.rc.future_fast_spots_departures[cs.charging_station_number].index(leaving_time)
                                del self.rc.cars_arriving_fast_spots_list[cs.charging_station_number][fast_spot_car_index]
                                del self.rc.future_fast_spots_arrivals[cs.charging_station_number][fast_spot_car_index]
                                del self.rc.future_fast_spots_departures[cs.charging_station_number][fast_spot_departure_index]

                    self.energy_units = 1000000


                # End charging
                if self.car_number == 1:
                    print("DONE: ", self.env.now)
                if self.car_number == 1:
                    print("FAST: ", is_fast_charging_spot)

                yield self.drive_to_location()
                trip_duration = random.randint(10000, 20000)
                self.energy_units = self.energy_units - trip_duration
                yield self.env.timeout(trip_duration)

                if self.car_number == 1:
                    print("AT_RAND_LOCATION: ", self.env.now)
            else:
                yield self.park()
