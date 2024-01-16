import random
import copy
from railnl import RailNL

max_aantal_trajecten = 7
max_aantal_minuten = 120    
baseline = RailNL()

baseline.load_stations('StationsHolland.csv')
baseline.load_connections('ConnectiesHolland.csv')
# Create a random procedure to select a amount of trajecten that is less than max aantal trajecten
aantal_trajecten = random.randint(1, max_aantal_trajecten)


# Adds a random amount of trajecten to the baseline, each with a random amount of stations. Each station is choosen randomly.
def random_algorithm(herhalingen):
    totaal_herhalingen = herhalingen
    baseline_at_max_score = None
    max_score = 0
    while herhalingen > 0:
        for i in range(1, aantal_trajecten + 1):
            baseline.create_traject(i)
            random_minuten_per_traject = random.randint(5, max_aantal_minuten)
            begin_station = random.choice(baseline.stations)
            baseline.trajecten[i].add_station_to_traject(begin_station)
            while True:
                if baseline.sum_time(i) < random_minuten_per_traject:
                    # Only possible stations are those in the connections, and those that are not already in the traject
                    list_possible_stations = [station for station in begin_station.connections if not baseline.trajecten[i].is_bereden(station)]
                    if list_possible_stations:
                        new_station = random.choice(list_possible_stations)
                        baseline.trajecten[i].add_station_to_traject(new_station)
                        begin_station = new_station
                    # if there are no possible stations, break the loop
                    else:
                        break
                else:
                    break
        # If the score is higher than the max score, save the baseline        
        if baseline.get_score() > max_score:
            max_score = baseline.get_score()
            baseline_at_max_score = copy.deepcopy(baseline)
        herhalingen -= 1 
        if herhalingen/totaal_herhalingen * 100 % 5 == 0:
            print(f"{herhalingen/totaal_herhalingen * 100}%")

    return baseline_at_max_score


random_test = random_algorithm(100)
# print_output(random_test)
print(random_test.get_score())
random_test.print_output()
random_test.upload_output('output.csv')