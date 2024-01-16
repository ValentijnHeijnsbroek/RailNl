from railnl import RailNL
import random
import copy
max_aantal_trajecten = 7


def greedy_algorithm(herhalingen):
    totaal_herhalingen = herhalingen
    greedy = RailNL()
    greedy.load_stations('StationsHolland.csv')
    greedy.load_connections('ConnectiesHolland.csv')
    greedy_at_max_score = None
    max_score = 0
    while herhalingen > 0:
        aantal_trajecten = random.randint(1, max_aantal_trajecten)
        for i in range(1, aantal_trajecten + 1):
            greedy.create_traject(i)
            begin_station = random.choice(greedy.stations)
            greedy.trajecten[i].add_station_to_traject(begin_station)
            # print(f"Begin station = {begin_station.name}")
            max_score_station = 0

            while max_score_station >= 0:
                list_possible_stations = [station for station in begin_station.connections if not greedy.trajecten[i].is_bereden(station)]
                max_score_station = 0
                if list_possible_stations:
                    # print("Possible stations: ")
                    best_station_name = ""
                    for station in list_possible_stations:
                        # print(station.name)
                        greedy.trajecten[i].add_station_to_traject(station)
                        greedy.get_score()
                        if greedy.get_score() > max_score_station:
                            max_score_station = greedy.get_score()
                            best_station_name = station.name
                        greedy.trajecten[i].delete_station(station)
                    best_station = greedy.get_station_by_name(best_station_name)
    
                    if best_station and max_score_station > 0:
                        greedy.trajecten[i].add_station_to_traject(best_station)
                    begin_station = best_station
                    # print(f"Best station = {best_station.name}")
                    # print(f"Last station in traject = {greedy.trajecten[i].traject_stations[-1].name}")
                    
                else:
                    break

        if greedy.get_score() > max_score:
            max_score = greedy.get_score()
            greedy_at_max_score = copy.deepcopy(greedy)
        herhalingen -= 1
        if herhalingen/totaal_herhalingen * 100 % 5 == 0:
            print(f"{herhalingen/totaal_herhalingen * 100}%")
    return greedy_at_max_score




greedy = greedy_algorithm(100)

print(greedy.get_score())
greedy.print_output()
greedy.upload_output('output_greedy.csv')

