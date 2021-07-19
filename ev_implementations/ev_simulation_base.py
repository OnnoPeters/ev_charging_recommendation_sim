from helper_files.simulation_parameters import NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR
import random
import abc
import numpy as np


class BaseEV(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, env, world_size, x_coordinate, y_coordinate, identifying_number, charging_stations, acceptance, normal_distributed_location_data_rate, normal_charging_factor, fast_charging_factor):
        self.env = env
        self.world_size = world_size
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.car_number = identifying_number
        self.charging_stations = charging_stations
        self.acceptance = acceptance
        self.normal_distributed_location_data_rate = normal_distributed_location_data_rate
        self.normal_charging_factor = normal_charging_factor
        self.fast_charging_factor = fast_charging_factor
        self.energy_units = 1000000
        self.way_to_destination = None
        self.destination = None
        self.charging_station_destination = None
        self.cs = None
        self.reactivate = env.event()
        self.deactivated = False
        self.parked = False
        self.action = env.process(self.run())

        #Monitoring data
        self.time_on_way_to_cs = 0
        self.charging_time = 0
        self.number_of_chargings = 0

    def park(self):
        """
        Deactivates this EV
        """
        return self.reactivate

    def continue_driving(self):
        """
        If this EV is deactivated, reactivates it.
        """
        if self.deactivated:
            self.deactivated = False
            self.reactivate.succeed()
            self.reactivate = self.env.event()

    def generate_random_destination(self):
        """
        Generates a random destination on the grid where this EV can drive to
        """
        if random.randint(0, 100) < 100 * self.normal_distributed_location_data_rate:
            x = -1
            y = -1
            while x < 0 or x >= self.world_size:
                x = int(np.random.normal(int(self.world_size / 2), int(self.world_size / 8)))
            while y < 0 or y >= self.world_size:
                y = int(np.random.normal(int(self.world_size / 2), int(self.world_size / 8)))
        else:
            x = random.randint(0, self.world_size - 1)
            y = random.randint(0, self.world_size - 1)
        self.destination = (x, y)

    def drive_to_location(self):
        """
        Lets EV drive to a destination.
        """
        if self.charging_station_destination is not None:
            selected_destination = self.charging_station_destination.get_location()
        else:
            selected_destination = self.destination
        distance = self.calculate_distance(selected_destination[0], selected_destination[1])
        self.energy_units -= distance
        self.x_coordinate = selected_destination[0]
        self.y_coordinate = selected_destination[1]
        return self.env.timeout(distance)

    def calculate_distance(self, x, y):
        """
        Calculates a distance between this EV and a given x and y coordinate
        """
        return abs(x - self.x_coordinate) + abs(y - self.y_coordinate)

    def start_charging(self, is_fast_charging_spot):
        """
        Make EV charge.
        """
        if is_fast_charging_spot:
            charging_time = int((1000000 - self.energy_units) * self.fast_charging_factor)
            #charging_time = np.random.normal(28800, 14400)
        else:
            charging_time = int((1000000 - self.energy_units) * self.normal_charging_factor)
            #charging_time = np.random.normal(5400, 3600)
            #charging_time = charging_time if charging_time > 0 else 0
        return self.env.timeout(charging_time)

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
                time_on_way_to_cs = self.calculate_distance(self.charging_station_destination.get_location()[0], self.charging_station_destination.get_location()[1])\
                                          + (abs(self.destination[0] - self.charging_station_destination.get_location()[0]) + abs(self.destination[1] - self.charging_station_destination.get_location()[1])) - direct_distance
                self.time_on_way_to_cs += time_on_way_to_cs

                self.number_of_chargings += 1

             #   if self.car_number == 1:
             #       print("DRIVING: ", self.env.now)
                yield self.drive_to_location()

                #Charging
                charging_spot = self.charging_station_destination.allocate_charging_spot()
                self.cs = self.charging_station_destination
                self.charging_station_destination = None

                start_waiting = self.env.now
                #if self.car_number == 1:
                 #   print("WAITING: ", self.env.now)
                #    print(self.time_on_way_to_cs)
                #    print(direct_distance)
                with charging_spot.request() as req:
                    yield req

                    start_charging = self.env.now
                #    if self.car_number == 1:
                #        print("CHARGING: ", self.env.now)
                #        print(self.waiting_time)
                    is_fast_charging_spot = self.cs.check_free_fast_spot()
                    if is_fast_charging_spot:
                        charging_time = int((1000000 - self.energy_units) * self.fast_charging_factor)
                    else:
                        charging_time = int((1000000 - self.energy_units) * self.normal_charging_factor)
                    self.charging_time += charging_time

                    yield self.start_charging(is_fast_charging_spot)
                    if is_fast_charging_spot:
                        self.cs.free_up_fast_spot()

                    self.energy_units = 1000000

                # End charging
               # if self.car_number == 1:
               #     print("DONE: ", self.env.now)
              #      print(self.charging_time)
                yield self.drive_to_location()
             #   if self.car_number == 1:
             #       print("DESTINATION: ", self.env.now)
             #       print(self.unproductive_time)

                trip_duration = random.randint(10000, 20000)
                self.energy_units = self.energy_units - trip_duration
                yield self.env.timeout(trip_duration)

                self.cs = None
            else:
                yield self.park()

    @abc.abstractmethod
    def set_charging_station_as_destination(self):
        """
        The charging station recommendation system will be added by inheriting classes here.
        """
        return
