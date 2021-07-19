import simpy
from helper_files.simulation_parameters import NUMBER_OF_FAST_CHARGERS


class ChargingStation(object):
    def __init__(self, env, x_coordinate, y_coordinate, identifying_number, car_capacity):
        self.env = env
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.charging_station_number = identifying_number
        self.car_capacity = car_capacity
        self.charging_spots = simpy.Resource(env, capacity=self.car_capacity)
        self.fast_charging_places = int(self.car_capacity * NUMBER_OF_FAST_CHARGERS)

    def get_location(self):
        """
        Gets location of this CS.
        """
        return self.x_coordinate, self.y_coordinate

    def allocate_charging_spot(self):
        """
        Returns a charging spot to a requesting EV or puts them in a queue for it.
        """
        return self.charging_spots

    def check_free_fast_spot(self):
        """
        Returns if a free fast spot is available.
        """
        if self.fast_charging_places > 0:
            self.fast_charging_places -= 1
            return True
        else:
            return False

    def free_up_fast_spot(self):
        """
        Signalizes that an EV has released a fast spot.
        """
        self.fast_charging_places += 1

    def get_number_of_free_spots(self):
        """
        Returns number of free spots.
        """
        return self.charging_spots.capacity - self.charging_spots.count

    def get_number_of_free_fast_spots(self):
        """
        Returns number of free fast spots.
        """
        return self.fast_charging_places

    def get_queue_size(self):
        """
        Returns queue size.
        """
        return len(self.charging_spots.queue)

    def get_number_of_cars(self):
        """
        Returns entire number of cars currently at this CS.
        """
        return self.charging_spots.count + len(self.charging_spots.queue)
