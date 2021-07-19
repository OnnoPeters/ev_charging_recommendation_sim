WORLD_SIZE = 10000   # Width and height of the grid
NUMBER_OF_CHARGING_STATIONS = 10   # Number of CS
NUMBER_OF_TOTAL_CARS = 1000    # Maximum number of EVs on the grid
ENV_ENTIRE_LENGTH = 172800    # How long cars should be active
LENGTH_OF_SIMULATION = 432000    # Total length of simulation
NUMBER_OF_REPETITIONS = 10    # Number of runs per strategy (MIN: 2)
CAPACITY_PER_CHARGING_STATION = 10    # How many chargers per CS
INFORMATION_TIME_UNIT_STEP_SIZE = 1000    # At which rate information for the plotting is taken
ADVICE_FOLLOW_RATE_FOR_NON_NEAREST_CS = 0.9   # Chance that users will listen to the recommendation if it is not the nearest CS (MIN: 0, MAX: 1)
NORMAL_DISTRIBUTED_DATA_RATE = 0.8   # How many CS and EV destinations are normally distributed (MIN: 0, MAX: 1)
NUMBER_OF_FAST_CHARGERS = 0.3    # Proportion of fast chargers from total chargers (MIN: 0, MAX: 1)
NORMAL_CHARGING_FACTOR = 0.6   # How many time units are needed to charge one energy unit
FAST_CHARGING_FACTOR = 0.1   # How many time units are needed to charge one energy unit
TIME_FACTOR = {     # Average proportion of total cars on the street per "hour"
    0: 0.4,
    1: 0.4,
    2: 0.4,
    3: 0.45,
    4: 0.5,
    5: 0.55,
    6: 0.7,
    7: 0.95,
    8: 0.95,
    9: 0.95,
    10: 0.9,
    11: 0.85,
    12: 0.8,
    13: 0.8,
    14: 0.85,
    15: 0.85,
    16: 0.95,
    17: 0.95,
    18: 0.9,
    19: 0.85,
    20: 0.75,
    21: 0.65,
    22: 0.55,
    23: 0.45
}
