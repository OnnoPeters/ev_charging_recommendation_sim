from ev_implementations.ev_no_charge import EVNoCharge
from ev_implementations.ev_simulation_nearest_cs import EVNearestCS
from ev_implementations.ev_least_frequented_cs import EVLeastFrequented
from ev_implementations.ev_nearest_free_spot_and_smallest_queue import EVCombined
from ev_implementations.ev_rc_equal_distribution import EVRCEqualDistribution
from ev_implementations.ev_random_charging_station import EVRandomCS
from ev_implementations.ev_nearest_with_free_fast_spot import EVNearestCSWithFreeFastSpot
from ev_implementations.ev_rc_best_by_average_time import EVRCBestByAverageTime
from cs_implementatons.cs_simulation_base import ChargingStation
from rc_implementations.rc_best_by_average_time_tracking import RCBestByAverageTime
from rc_implementations.rc_equal_distribution import RCEqualDistribution
from helper_files.plotting import plot_nice_line_graph, plot_nice_bar_graph, plot_nice_heatmap
from helper_files.generating_methods import generate_charging_station_locations, run_simulation, run_simulation_with_rc, run_simulate_car_behaviour, run_simulation_parameters, run_simulation_rc_parameters, generate_charging_station_locations_parameters
from helper_files.simulation_parameters import LENGTH_OF_SIMULATION, NUMBER_OF_TOTAL_CARS, NUMBER_OF_CHARGING_STATIONS, WORLD_SIZE,\
    NUMBER_OF_REPETITIONS, CAPACITY_PER_CHARGING_STATION, INFORMATION_TIME_UNIT_STEP_SIZE, ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS, \
    NORMAL_DISTRIBUTED_DATA_RATE, NUMBER_OF_FAST_CHARGERS, NORMAL_CHARGING_FACTOR, FAST_CHARGING_FACTOR, ENV_ENTIRE_LENGTH
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Generates the charging station locations for all runs before to make them comparable.
    charging_station_locations = generate_charging_station_locations()

    choice = input("1: Show only car behaviour \n"
                   "2: Compare EVs \n")
    # Show car behaviour
    if choice == '1':
        show_car_behaviour(charging_station_locations)

    elif choice == '2':
        with open('results\\results.txt', 'w') as file:
            file.write("Results: \n")
            file.write("WORLD_SIZE = {} \n".format(WORLD_SIZE))
            file.write("NUMBER_OF_CHARGING_STATIONS = {} \n".format(NUMBER_OF_CHARGING_STATIONS))
            file.write("NUMBER_OF_TOTAL_CARS = {} \n".format(NUMBER_OF_TOTAL_CARS))
            file.write("LENGTH_OF_SIMULATION = {} \n".format(LENGTH_OF_SIMULATION))
            file.write("ACTIVE LENGTH = {} \n".format(ENV_ENTIRE_LENGTH))
            file.write("NUMBER_OF_REPETITIONS = {} \n".format(NUMBER_OF_REPETITIONS))
            file.write("CAPACITY_PER_CHARGING_STATION = {} \n".format(CAPACITY_PER_CHARGING_STATION))
            file.write("INFORMATION_TIME_UNIT_STEP_SIZE = {} \n".format(INFORMATION_TIME_UNIT_STEP_SIZE))
            file.write("ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS = {} \n".format(ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS))
            file.write("NORMAL_DISTRIBUTED_DATA_RATE = {} \n".format(NORMAL_DISTRIBUTED_DATA_RATE))
            file.write("NUMBER_OF_FAST_CHARGERS = {} \n".format(NUMBER_OF_FAST_CHARGERS))
            file.write("NORMAL_CHARGING_FACTOR = {} \n".format(NORMAL_CHARGING_FACTOR))
            file.write("FAST_CHARGING_FACTOR = {} \n \n".format(FAST_CHARGING_FACTOR))

        show_car_behaviour(charging_station_locations)

        # Decentralized - Cars can only get information from charging stations, charging stations only know about cars currently charging and cars in queue
        monitoringEVRandomCS = run_simulation(EVRandomCS, ChargingStation, charging_station_locations)
        monitoringEVRandomCS.print_new_information()
        monitoringEVNearestCS = run_simulation(EVNearestCS, ChargingStation, charging_station_locations)
        monitoringEVNearestCS.print_new_information()
        monitoringEVLeastFrequented = run_simulation(EVLeastFrequented, ChargingStation, charging_station_locations)
        monitoringEVLeastFrequented.print_new_information()
        monitoringEVNearestCSWithFreeFastSpot = run_simulation(EVNearestCSWithFreeFastSpot, ChargingStation, charging_station_locations)
        monitoringEVNearestCSWithFreeFastSpot.print_new_information()
        monitoringEVCombined = run_simulation(EVCombined, ChargingStation, charging_station_locations)
        monitoringEVCombined.print_new_information()

        # Centralized - Central recommendation server knows every cars location and to which charging station they are going, as well as the cars in charging and in the queue of each charging station
        monitoringEVRCBestByAverageTime = run_simulation_with_rc(EVRCBestByAverageTime, ChargingStation, RCBestByAverageTime, charging_station_locations)
        monitoringEVRCBestByAverageTime.print_new_information()
        monitoringEVRCEqualDistribution = run_simulation_with_rc(EVRCEqualDistribution, ChargingStation, RCEqualDistribution, charging_station_locations)
        monitoringEVRCEqualDistribution.print_new_information()

        compare_simulations([monitoringEVRandomCS, monitoringEVNearestCS, monitoringEVNearestCSWithFreeFastSpot, monitoringEVLeastFrequented, monitoringEVCombined, monitoringEVRCBestByAverageTime, monitoringEVRCEqualDistribution])

    elif choice == "3":
        test_performances()


def show_car_behaviour(charging_station_locations):
    """
    Plots the behavior of the cars and the location of the cars and the charging stations.
    Also shows the effect the time units have on the EV distribution.
    """
    monitoringEVNoCharge = run_simulate_car_behaviour(EVNoCharge, ChargingStation, charging_station_locations)
    plot_nice_heatmap(monitoringEVNoCharge.car_locations, "EV Distribution")
    plot_nice_heatmap(monitoringEVNoCharge.get_cs_locations_in_array(), "CS Distribution")
    x = np.arange(0, len(monitoringEVNoCharge.number_of_active_cars))
    plot_nice_line_graph(x, [monitoringEVNoCharge.number_of_active_cars], "Number of cars active on the streets", None, "Time units", "Number of cars active", 0, 173, 0, NUMBER_OF_TOTAL_CARS)


def compare_simulations(monitoring_list):
    """
    Compares simulations by plotting the data against each other.
    """

    # Plots waiting time, driving time, charging time and unproductive time
    x = np.arange(0, LENGTH_OF_SIMULATION if LENGTH_OF_SIMULATION % INFORMATION_TIME_UNIT_STEP_SIZE == 0 else LENGTH_OF_SIMULATION - INFORMATION_TIME_UNIT_STEP_SIZE, INFORMATION_TIME_UNIT_STEP_SIZE)
    unproductive_time_all = []
    avg_waiting_time_all = []
    avg_time_to_cs_all = []
    avg_charging_time_all = []
    labels = []
    for i in range(len(monitoring_list)):
        unproductive_time_by_charging_operation, avg_waiting_time_by_charging_operation, avg_time_to_cs_by_charging_operation, avg_charging_time_by_charging_operation = monitoring_list[i].calculate_unproductive_time()
        unproductive_time_all.append(unproductive_time_by_charging_operation)
        avg_waiting_time_all.append(avg_waiting_time_by_charging_operation)
        avg_time_to_cs_all.append(avg_time_to_cs_by_charging_operation)
        avg_charging_time_all.append(avg_charging_time_by_charging_operation)
        labels.append(monitoring_list[i].ev_class.__name__)

    plot_nice_line_graph(x, avg_waiting_time_all, "Time spent waiting per charging operation", labels, "Time", "Waiting time per charging operation")
    plot_nice_line_graph(x, avg_time_to_cs_all, "Time spent driving per charging operation", labels, "Time", "Driving time per charging operation")
    plot_nice_line_graph(x, avg_charging_time_all, "Time spent charging per charging operation", labels, "Time", "Charging time per charging operation")
    plot_nice_line_graph(x, unproductive_time_all, "Unproductive time per charging operation", labels, "Time", "Unproductive time per charging operation")

    # NOT USED
    #combined_charging_all = []
    #combined_queue_all = []
    #combined_driving_all = []
    #for i in range(len(monitoring_list)):
    #    combined_charging_size, combined_queue_size, combined_driving_to_cs_size, _, __ = monitoring_list[i].calculate_cs_data()
    #    combined_charging_all.append(np.divide(combined_charging_size, (NUMBER_OF_CHARGING_STATIONS * CAPACITY_PER_CHARGING_STATION * NUMBER_OF_REPETITIONS)))
    #    combined_queue_all.append(np.divide(combined_queue_size, (NUMBER_OF_CHARGING_STATIONS * CAPACITY_PER_CHARGING_STATION * NUMBER_OF_REPETITIONS)))
    #    combined_driving_all.append(np.divide(combined_driving_to_cs_size, (NUMBER_OF_CHARGING_STATIONS * CAPACITY_PER_CHARGING_STATION * NUMBER_OF_REPETITIONS)))

    #plot_nice_line_graph(x, combined_charging_all, "Amount of cars charging per charging spot", labels, "Time", "Cars charging per charging spot", 0, 173000, 0, 1)

    #plot_nice_line_graph(x, combined_queue_all, "Amount of cars waiting per charging spot", labels, "Time", "Cars waiting per charging spot")

    #plot_nice_line_graph(x, combined_driving_all, "Amount of cars driving to CS per charging spot", labels, "Time", "Cars driving to CS per charging spot")

    # Plots average amount of cars per CS
    x = np.arange(0, NUMBER_OF_CHARGING_STATIONS)
    avg_amount_of_cars_waiting_per_charging_spot_all = []
    avg_amount_of_cars_charging_per_charging_spot_all = []
    max_y = 0
    for i in range(len(monitoring_list)):
        _, __, ___, avg_amount_of_cars_waiting_per_charging_spot, avg_amount_of_cars_charging_per_charging_spot = monitoring_list[i].calculate_cs_data()
        avg_amount_of_cars_waiting_per_charging_spot_all.append(avg_amount_of_cars_waiting_per_charging_spot)
        avg_amount_of_cars_charging_per_charging_spot_all.append(avg_amount_of_cars_charging_per_charging_spot)

        max_y = max(max_y, max(avg_amount_of_cars_waiting_per_charging_spot) + 10)

    for i in range(len(monitoring_list)):
        plot_nice_bar_graph(x, avg_amount_of_cars_charging_per_charging_spot_all[i], avg_amount_of_cars_waiting_per_charging_spot_all[i],
                            "Amount of cars charging per charging station ({})".format(monitoring_list[i].ev_class.__name__), "Charging station number", "Amount of cars charging (avg)", 0, max_y)





















#
# NOT USED HERE
#
def test_performances():
    parameter_list_to_change = [5, 10, 20, 50, 100]
    #parameter2_list_to_change = [0.01, 0.02, 0.1, 0.2, 0.4, 1, 2, 6, 10]
    results = []
    for i in range(4):
         results.append(np.zeros(len(parameter_list_to_change)))

    result_counter = 0
    for parameter in parameter_list_to_change:
        charging_station_locations = generate_charging_station_locations_parameters(parameter)
        print("Parameter run ", result_counter + 1)
        number_of_cs = parameter
        number_of_total_cars = NUMBER_OF_TOTAL_CARS
        normal_charging_factor = NORMAL_CHARGING_FACTOR
        fast_charging_factor = FAST_CHARGING_FACTOR
        capacity_per_cs = CAPACITY_PER_CHARGING_STATION

        monitoringEVRandomCS = run_simulation_parameters(EVRandomCS, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCS = run_simulation_parameters(EVNearestCS, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCSWithFreeFastSpot = run_simulation_parameters(EVNearestCSWithFreeFastSpot, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)
        monitoringEVNearestCSWithFreeCSAndSmallestQueue = run_simulation_parameters(EVLeastFrequented, ChargingStation, charging_station_locations, number_of_total_cars, number_of_cs, normal_charging_factor, fast_charging_factor, capacity_per_cs)


        results[0][result_counter] = monitoringEVRandomCS.unproductive_time[-1] / monitoringEVRandomCS.number_of_chargings[-1]
        results[1][result_counter] = monitoringEVNearestCS.unproductive_time[-1] / monitoringEVNearestCS.number_of_chargings[-1]
        results[2][result_counter] = monitoringEVNearestCSWithFreeFastSpot.unproductive_time[-1] /monitoringEVNearestCSWithFreeFastSpot.number_of_chargings[-1]
        results[3][result_counter] = monitoringEVNearestCSWithFreeCSAndSmallestQueue.unproductive_time[-1] / monitoringEVNearestCSWithFreeCSAndSmallestQueue.number_of_chargings[-1]
        result_counter += 1

    name_list = ["Random", "Nearest", "CS with Free Fast Spot", "Least Frequented CS" ]# "Smallest Amount of Time Lost", "Equal Distribution"]

    for n in range(len(name_list)):
        plt.plot(parameter_list_to_change, results[n], label=str(name_list[n]))
    plt.title("Unproductive time comparison")
    plt.legend(loc="upper left")
    plt.show()



if __name__ == "__main__":
    main()
