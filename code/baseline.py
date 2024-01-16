import random
from railnl import RailNL

max_aantal_trajecten = 6
max_aantal_minuten = 120    
baseline = RailNL()

baseline.load_stations('StationsHolland.csv')
baseline.load_connections('ConnectiesHolland.csv')
# Create a random procedure to select a amount of trajecten that is less than max aantal trajecten
aantal_trajecten = random.randint(1, max_aantal_trajecten)


# Adds a random amount of trajecten to the baseline, each with a random amount of stations. Each station is choosen randomly.

for i in range(1, aantal_trajecten + 1):
    baseline.create_traject(i)
    random_minuten_per_traject = random.randint(5, max_aantal_minuten)
    begin_station = random.choice(baseline.stations)
    baseline.trajecten[i].add_station_to_traject(begin_station)
    while True:
        if baseline.sum_time(i) < random_minuten_per_traject:
            # list_possible_stations = list(begin_station.connections)
            list_possible_stations = [station for station in begin_station.connections if not baseline.trajecten[i].is_bereden(station)]
            if list_possible_stations:
                new_station = random.choice(list_possible_stations)
                baseline.trajecten[i].add_station_to_traject(new_station)
                begin_station = new_station
            else:
                break
        
        else:
            break

    # connection_index = random.choice(1, len(begin_station.connections))
    # print(begin_station.name)


for j in range(1, len(baseline.trajecten) +1 ):
    print(f"Traject: {j}")
    for i in range(len(baseline.trajecten[j].traject_stations)):
        print(baseline.trajecten[j].traject_stations[i].name)
    print(f"Duration for traject {j}: {baseline.sum_time(j)}")
    print(" ")
print(f"Score: {baseline.get_score()}")



    
    

# for i in range(aantal_trajecten):
#     baseline.create_traject(i)
#     random_minuten_per_traject = random.randint(5, max_aantal_minuten)
#     begin_station = random.choice(baseline.stations)
#     baseline.trajecten[i].add_station_to_traject(begin_station)
#     while True:
#         if baseline.sum_time(i) < random_minuten_per_traject:
#             list_possible_stations = list(begin_station.connections)
#             for station in list_possible_stations:
#                 if baseline.trajecten[i].is_bereden(station):
#                     list_possible_stations.remove(station)
#                     print(f"Station {station.name} removed")
#             print("After removed the possible stations are:")
#             for j in range(len(list_possible_stations)):
#                 print(list_possible_stations[j].name)
#             print(" ")
#             if not list_possible_stations:

#                 break

#             connection_station = random.choice(list_possible_stations)
#             baseline.trajecten[i].add_station_to_traject(connection_station)
#             begin_station = connection_station

        # else:
        #     break