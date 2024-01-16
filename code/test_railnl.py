# test_railnl.py

import pytest
from railnl import RailNL
  # Assuming your main class is in a file named railnl.py

@pytest.fixture
def rail_nl_instance():
    rail_nl = RailNL()
    rail_nl.load_stations('StationsHolland.csv')
    rail_nl.load_connections('ConnectiesHolland.csv')
    return rail_nl

def test_load_stations(rail_nl_instance):
    assert len(rail_nl_instance.stations) > 0

def test_load_connections(rail_nl_instance):
    for i in range(len(rail_nl_instance.stations)):
        assert len(rail_nl_instance.stations[1].connections) > 0


def test_create_traject(rail_nl_instance):
    traject_count_before = len(rail_nl_instance.trajecten)
    rail_nl_instance.create_traject(0)
    traject_count_after = len(rail_nl_instance.trajecten)
    assert traject_count_after == traject_count_before + 1


def test_stations_in_traject(rail_nl_instance):
    rail_nl_instance.create_traject(1)
    Amsterdam_Centraal = rail_nl_instance.get_station_by_name('Amsterdam Centraal')
    Amsterdam_Amstel = rail_nl_instance.get_station_by_name('Amsterdam Amstel')
    Amsterdam_Zuid = rail_nl_instance.get_station_by_name('Amsterdam Zuid')
    rail_nl_instance.trajecten[1].add_station_to_traject(Amsterdam_Centraal)
    rail_nl_instance.trajecten[1].add_station_to_traject(Amsterdam_Amstel)
    rail_nl_instance.trajecten[1].add_station_to_traject(Amsterdam_Zuid)

    assert rail_nl_instance.trajecten[1].traject_stations[0] == Amsterdam_Centraal
    assert rail_nl_instance.trajecten[1].traject_stations[1] == Amsterdam_Amstel
    assert rail_nl_instance.trajecten[1].traject_stations[2] == Amsterdam_Zuid
    assert rail_nl_instance.sum_time(1) == 18




# Add more tests as needed

if __name__ == '__main__':
    pytest.main()
