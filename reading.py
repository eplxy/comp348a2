import json


class BaseStation:
    count = 0

    def __init__(self, lat, lon, ants):
        self.lat = lat
        self.lon = lon
        self.ants = ants


class Antenna:
    def __init__(self, frq, bw, pts):
        self.frq = frq
        self.bw = bw
        self.pts = pts


def read_file(file_path):
    file = open(file_path, "r")
    data = json.loads(file.read())
    return data


def parse_settings(data):
    return
    # min lat, max lat, min lon, max lon, step.


def parse_stations(data):
    return
    # list of stations
