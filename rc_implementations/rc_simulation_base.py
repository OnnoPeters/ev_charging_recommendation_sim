import abc
import numpy as np


class RecommendationCenter:
    __metaclass__ = abc.ABCMeta

    def __init__(self, env, charging_stations, cars, capacity, number_of_fast_chargers):
        self.env = env
        self.charging_stations = charging_stations
        self.cars = cars
        self.capacity = capacity
        self.number_of_fast_chargers = number_of_fast_chargers
        self.future_cs_arrivals = []
        self.future_cs_departures = []
        self.future_fast_spots_arrivals = []
        self.future_fast_spots_departures = []
        self.cars_arriving_list = []
        self.cars_arriving_fast_spots_list = []
        self.waiting_time_per_cs = np.zeros(len(charging_stations))
        self.charging_time_per_cs = np.zeros(len(charging_stations))
        self.number_of_chargings_per_cs = np.zeros(len(charging_stations))
        for i in range(len(charging_stations)):
            self.future_cs_arrivals.append([])
            self.future_cs_departures.append([])
            self.future_fast_spots_arrivals.append([])
            self.future_fast_spots_departures.append([])
            self.cars_arriving_list.append([])
            self.cars_arriving_fast_spots_list.append([])


    @abc.abstractmethod
    def recommend_charging_station(self, car):
        """
        Overwritten in each inherited recommendation center to implement the strategy.
        """
        return

    def get_cs_occupation(self, cs_number, time):
        """
        Get predicted number of cars at the given time at given CS.
        """
        occupation = len([x for x in self.future_cs_arrivals[cs_number] if x <= time]) - len([x for x in self.future_cs_departures[cs_number] if x < time])
        return occupation if occupation >= 0 else 0

    def get_fast_spot_occupation(self, cs_number, time):
        """
        Get predicted number of cars at fast spots at the given time at given CS.
        """
        occupation = len([x for x in self.future_fast_spots_arrivals[cs_number] if x <= time]) - len([x for x in self.future_fast_spots_departures[cs_number] if x < time])
        return occupation if occupation >= 0 else 0

    def get_cs_arrival_and_departure_list(self, cs_number, time):
        """
        Get the times of predicted arrivals and departures of cars at the given time and at the given CS.
        """
        departures = [x for x in self.future_cs_departures[cs_number] if x < time]
        return [x for x in self.future_cs_arrivals[cs_number] if x <= time and x not in departures]

    def get_fast_spots_arrival_and_departure_list(self, cs_number, time):
        """
        Get the times of predicted arrivals and departures of cars at fast spots at the given time and at the given CS.
        """
        departures = [x for x in self.future_fast_spots_departures[cs_number] if x < time]
        return [x for x in self.future_fast_spots_arrivals[cs_number] if x <= time and x not in departures]

    def add_charging_to_cs(self, cs_number):
        """
        Add a charging car to the given CS.
        """
        self.number_of_chargings_per_cs[cs_number] += 1

    def add_charging_time_to_cs(self, cs_number, time):
        """
        Add the given charging time to the given CS.
        """
        self.charging_time_per_cs[cs_number] += time

    def add_waiting_time_to_cs(self, cs_number, time):
        """
            Add the given waiting time to the given CS.
        """
        self.waiting_time_per_cs[cs_number] += time

    def get_avg_charging_time_for_cs(self, cs_number):
        """
        Get the average charging time for the given CS.
        """
        return self.charging_time_per_cs[cs_number] / (self.number_of_chargings_per_cs[cs_number] + 1)

    def get_avg_waiting_time_for_cs(self, cs_number):
        """
        Get the average waiting time for the given CS.
        """
        return self.waiting_time_per_cs[cs_number] / (self.number_of_chargings_per_cs[cs_number] + 1)







