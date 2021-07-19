from helper_files.simulation_parameters import TIME_FACTOR, ENV_ENTIRE_LENGTH
import numpy as np

class SimulationController:
    def __init__(self, env, cars, charging_stations, rc):
        self.env = env
        self.cars = cars
        self.charging_stations = charging_stations
        self.action = env.process(self.control_time_factor())
        self.rc = rc

    def control_time_factor(self):
        while True:
            if (self.env.now / 60) % 60 == 0:
                time_factor_current = TIME_FACTOR[((self.env.now/60)/60) % 24]
                cars_needed = np.random.normal(time_factor_current * len(self.cars), len(self.cars) / 50)
                for car in self.cars:
                    if self.env.now <= ENV_ENTIRE_LENGTH:
                        if car.car_number > cars_needed:
                            car.deactivated = True
                        else:
                            car.continue_driving()
                    else:
                        car.deactivated = True
            #if self.env.now % 100:

            yield self.env.timeout(100)