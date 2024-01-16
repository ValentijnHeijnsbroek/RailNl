from railnl import RailNL

def initialize_rail():
    rail_nl = RailNL()
    rail_nl.load_stations('StationsNationaal.csv')
    rail_nl.load_connections('ConnectiesNationaal.csv')
    return rail_nl
