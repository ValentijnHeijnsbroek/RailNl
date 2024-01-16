# test_railnl.py

import pytest
from railnl import RailNL
from station import Station
from traject import Traject
  # Assuming your main class is in a file named railnl.py

@pytest.fixture
def rail_nl_instance():
    return RailNL()

def test_load_stations(rail_nl_instance):
    rail_nl_instance.load_stations('StationsHolland.csv')  # Provide a test station file
    assert len(rail_nl_instance.stations) > 0

def test_load_connections(rail_nl_instance):
    rail_nl_instance.load_connections('ConnectiesHolland.csv')  # Provide a test connections file
    for i in range(len(rail_nl_instance.stations)):
        assert len(rail_nl_instance.stations[1].connections) > 0


def test_create_traject(rail_nl_instance):
    traject_count_before = len(rail_nl_instance.trajecten)
    rail_nl_instance.create_traject(0)
    traject_count_after = len(rail_nl_instance.trajecten)
    assert traject_count_after == traject_count_before + 1

def test_stations_in_traject(rail_nl_instance):
    new_traject = rail_nl_instance.create_traject(1)
    Alkmaar = rail_nl_instance.get_station_by_name('Alkmaar')
    Hoorn = rail_nl_instance.get_station_by_name('Hoorn')
    new_traject.add_station(Alkmaar)
    new_traject.add_station(Hoorn)
    assert rail_nl_instance.trajecten[1] == new_traject
    


# Add more tests as needed

if __name__ == '__main__':
    pytest.main()
