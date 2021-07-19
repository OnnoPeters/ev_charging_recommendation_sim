import random
from helper_files.simulation_parameters import LENGTH_OF_SIMULATION, NUMBER_OF_TOTAL_CARS, NUMBER_OF_CHARGING_STATIONS, WORLD_SIZE,\
    NUMBER_OF_REPETITIONS, CAPACITY_PER_CHARGING_STATION, INFORMATION_TIME_UNIT_STEP_SIZE, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, \
    NORMAL_DISTRIBUTED_DATA_RATE, NUMBER_OF_FAST_CHARGERS, NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR, ENV_ENTIRE_LENGTH
from helper_files.simulation_metrics import Monitoring
from helper_files.simulation_controller import SimulationController
import simpy
import numpy as np


def generate_charging_station_locations():

    charging_station_locations = []
    for i in range(NUMBER_OF_REPETITIONS):
        location_per_run = []
        for j in range(NUMBER_OF_CHARGING_STATIONS):
            while True:
                if random.randint(0, 100) < 100 * NORMAL_DISTRIBUTED_DATA_RATE:
                    x = -1
                    y = -1
                    while x < 0 or x >= WORLD_SIZE:
                        x = int(np.random.normal(int(WORLD_SIZE / 2), int(WORLD_SIZE / 8)))
                    while y < 0 or y >= WORLD_SIZE:
                        y = int(np.random.normal(int(WORLD_SIZE / 2), int(WORLD_SIZE / 8)))
                else:
                    x = random.randint(0, WORLD_SIZE - 1)
                    y = random.randint(0, WORLD_SIZE - 1)
                if (x, y) not in location_per_run:
                    location_per_run.append((x, y))
                    break

        charging_station_locations.append(location_per_run)

    return charging_station_locations


def generate_charging_stations(env, cs, charging_station_locations):
    charging_stations = []
    for i in range(NUMBER_OF_CHARGING_STATIONS):
        charging_stations.append(cs(env, charging_station_locations[i][0], charging_station_locations[i][1], i, CAPACITY_PER_CHARGING_STATION))
    return charging_stations


def generate_cars(ev, env, charging_stations):
    cars = []
    for i in range(NUMBER_OF_TOTAL_CARS):
        cars.append(ev(env, WORLD_SIZE, random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE), i, charging_stations, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, NORMAL_DISTRIBUTED_DATA_RATE, NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR))
    return cars


def generate_simulation_controller(env, cars, charging_stations):
    return SimulationController(env, cars, charging_stations)


def generate_rc(type_of_rc, env, charging_stations, cars):
    return type_of_rc(env, charging_stations, cars, CAPACITY_PER_CHARGING_STATION, int(CAPACITY_PER_CHARGING_STATION * NUMBER_OF_FAST_CHARGERS))


def run_simulate_car_behaviour(type_of_ev, type_of_cs, charging_station_locations):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            NUMBER_OF_CHARGING_STATIONS, NUMBER_OF_TOTAL_CARS, WORLD_SIZE)

    env = simpy.Environment()

    charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[0])
    cars = generate_cars(type_of_ev, env, charging_stations)
    simulation_controller = generate_simulation_controller(env, cars, charging_stations)
    env.process(monitoring.save_car_data(env))
    monitoring.initialize_monitoring_process(env, charging_stations, cars)

    env.run(until=LENGTH_OF_SIMULATION)

    return monitoring


def run_simulation(type_of_ev, type_of_cs, charging_station_locations):
    #metrics = Metrics(NUMBER_OF_CARS, NUMBER_OF_CHARGING_STATIONS, LENGTH_OF_SIMULATION, NUMBER_OF_REPETITIONS, CAPACITY_PER_CHARGING_STATION)
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH, NUMBER_OF_CHARGING_STATIONS, NUMBER_OF_TOTAL_CARS, WORLD_SIZE)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[i])
        cars = generate_cars(type_of_ev, env, charging_stations)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_with_rc(type_of_ev, type_of_cs, type_of_rc, charging_station_locations):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH, NUMBER_OF_CHARGING_STATIONS, NUMBER_OF_TOTAL_CARS, WORLD_SIZE)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations(env, type_of_cs, charging_station_locations[i])
        cars = generate_cars(type_of_ev, env, charging_stations)
        rc = generate_rc(type_of_rc, env, charging_stations, cars)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        for car in cars:
            car.get_recommendation_center(rc)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_rc_parameters(type_of_ev, type_of_cs, type_of_rc, charging_station_locations, number_of_cars, number_of_cs,normal_charging_factor, fast_charging_factor, capacity_per_cs):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            number_of_cs, number_of_cars, WORLD_SIZE)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations_parameters(env, type_of_cs, charging_station_locations[i], number_of_cs, capacity_per_cs)
        cars = generate_cars_parameters(type_of_ev, env, charging_stations, normal_charging_factor, fast_charging_factor)
        rc = generate_rc(type_of_rc, env, charging_stations, cars)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)
        for car in cars:
            car.get_recommendation_center(rc)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def run_simulation_parameters(type_of_ev, type_of_cs, charging_station_locations, number_of_cars, number_of_cs,normal_charging_factor, fast_charging_factor, capacity_per_cs):
    monitoring = Monitoring(type_of_ev, INFORMATION_TIME_UNIT_STEP_SIZE, LENGTH_OF_SIMULATION, ENV_ENTIRE_LENGTH,
                            number_of_cs, number_of_cars, WORLD_SIZE)

    for i in range(NUMBER_OF_REPETITIONS):
        env = simpy.Environment()

        charging_stations = generate_charging_stations_parameters(env, type_of_cs, charging_station_locations[i], number_of_cs, capacity_per_cs)
        cars = generate_cars_parameters(type_of_ev, env, charging_stations, number_of_cars, normal_charging_factor, fast_charging_factor)
        simulation_controller = generate_simulation_controller(env, cars, charging_stations)

        monitoring.initialize_monitoring_process(env, charging_stations, cars)
        monitoring.start_timing(env)

        env.run(until=LENGTH_OF_SIMULATION)
        print("Finished run {}".format(i + 1))

    return monitoring


def generate_cars_parameters(ev, env, charging_stations, number_of_cars, normal_charging_factor, fast_charging_factor):
    cars = []
    for i in range(number_of_cars):
        cars.append(ev(env, WORLD_SIZE, random.randint(0, WORLD_SIZE), random.randint(0, WORLD_SIZE), i, charging_stations, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, NORMAL_DISTRIBUTED_DATA_RATE, normal_charging_factor, fast_charging_factor))
    return cars


def generate_charging_stations_parameters(env, cs, charging_station_locations, number_of_cs, capacity_per_cs):
    charging_stations = []
    for i in range(number_of_cs):
        charging_stations.append(cs(env, charging_station_locations[i][0], charging_station_locations[i][1], i, capacity_per_cs))
    return charging_stations


def generate_charging_station_locations_parameters(number_of_charging_stations):
    charging_station_locations = []
    for i in range(NUMBER_OF_REPETITIONS):
        location_per_run = []
        for j in range(number_of_charging_stations):
            while True:
                if random.randint(0, 100) < 100 * NORMAL_DISTRIBUTED_DATA_RATE:
                    x = -1
                    y = -1
                    while x < 0 or x >= WORLD_SIZE:
                        x = int(np.random.normal(int(WORLD_SIZE / 2), int(WORLD_SIZE / 8)))
                    while y < 0 or y >= WORLD_SIZE:
                        y = int(np.random.normal(int(WORLD_SIZE / 2), int(WORLD_SIZE / 8)))
                else:
                    x = random.randint(0, WORLD_SIZE - 1)
                    y = random.randint(0, WORLD_SIZE - 1)
                if (x, y) not in location_per_run:
                    location_per_run.append((x, y))
                    break

        charging_station_locations.append(location_per_run)

    return charging_station_locations

