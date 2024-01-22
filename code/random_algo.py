import random
import copy
from railnl import RailNL
max_aantal_trajecten = 20
max_aantal_minuten = 180   
# Create a random procedure to select a amount of trajecten that is less than max aantal trajecten

# Adds a random amount of trajecten to the baseline, each with a random amount of stations. Each station is choosen randomly.
def random_algorithm(herhalingen):
    totaal_herhalingen = herhalingen
    baseline_at_max_score = RailNL()
    max_score = 0
    baseline_at_min_score = RailNL()
    min_score = 10000
    while herhalingen > 0:
        aantal_trajecten = random.randint(1, max_aantal_trajecten)
        baseline = RailNL()
        baseline.load_stations('StationsNationaal.csv')
        baseline.load_connections('ConnectiesNationaal.csv')
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
            baseline_at_max_score = baseline
        if baseline.get_score() < min_score:
            min_score = baseline.get_score()
            baseline_at_min_score = baseline
            
        herhalingen -= 1 
        if herhalingen/totaal_herhalingen * 100 % 1 == 0:
            print(f"{herhalingen/totaal_herhalingen * 100}%")

    return baseline_at_max_score
    # return baseline_at_max_score, baseline_at_min_score

baseline = random_algorithm(100000)
print(baseline.get_score())

# random_test = random_algorithm(10000)
#  #print_output(random_test)
# print(random_test.get_score())
# random_test.print_output()
# random_test.upload_output('output.csv')