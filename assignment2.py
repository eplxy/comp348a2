import textwrap
import random
import json
import math
import sys

FILE_PATH = "test.json"
data = {}
stations = {}
area = int()
station_ids = []


def read_file(file_path=FILE_PATH):
    file = open(file_path, "r")
    file_data = json.loads(file.read())
    return file_data


def load_data():
    global data, stations, area, station_ids
    if len(sys.argv) > 1:
        data = read_file(sys.argv[1])
    else:
        data = read_file()

    stations = data.get("baseStations")
    area = round(((abs(data.get('max_lat') - data.get('min_lat')) + data.get('step')) / data.get('step')) * (
            (abs(data.get('max_lon') - data.get('min_lon')) + data.get('step')) / data.get('step')))
    station_ids = [station['id'] for station in data.get("baseStations")]


def main():
    load_data()

    while True:
        choice = show_main_menu()
        if choice == "1":
            show_global_statistics()
        elif choice == "2":
            option_station_statistics()
        elif choice == "3":
            option_check_coverage()
        elif choice == "4":
            print("Exiting")
            break
        else:
            print("Invalid choice")
    return


def show_main_menu():
    print(textwrap.dedent("""
        ---------Main Menu---------
        1. Display Global Statistics
        2. Display Base Station Statistics
        3. Check Coverage
        4. Exit
          """))
    return input("Enter choice: ")


def show_global_statistics():
    stats = get_global_stats()
    print("Showing statistics for all stations under the provider")
    print("Total number of base stations:", stats.get('a'))
    print("Total number of antennas:", stats.get('b'))
    print("Maximum, minimum, and average number of antennas per base station:", stats.get('c'))
    print("Total number of points covered by exactly one antenna:", stats.get('d'))
    print("Total number of points covered by multiple antennas:", stats.get('e'))
    print("Total number of points not covered by any antenna:", stats.get('f'))
    print("Maximum number of antennas covering a single point:", stats.get('g'))
    print("Average number of antennas covering a single point:", stats.get('h'))
    print("Percentage of area covered by the base stations:", stats.get('i'), "%")
    print(f"Antenna with greatest coverage: Base Station {stats.get('j')[0]}, Antenna {stats.get('j')[1]}")


def get_global_stats():
    stats = {'a': int(), 'b': int(), 'c': (int(), int(), int()),
             'd': int(), 'e': int(), 'f': int(), 'g': int(),
             'h': float(), 'i': float(), 'j': (int(), int())
             }
    ant_stats = get_global_antenna_stats()
    stats['a'] = len(data.get("baseStations"))
    stats['b'] = get_global_ant_count()
    stats['c'] = (ant_stats['max'], ant_stats['min'], ant_stats['avg'])
    (single, multi) = get_global_coverage()
    stats['d'] = len(single)
    stats['e'] = len(set(multi))
    stats['f'] = area - stats['e'] - stats['d']
    multi_occurrences = occurrence_dict(multi)
    stats['g'] = (
        (0 if len(single) == 0 else 1) if len(
            multi_occurrences) == 0 else max(
            multi_occurrences.values())
    )
    stats['h'] = get_average_antenna_per_point(single, multi)
    stats['i'] = round(100 * (float(stats['d'] + stats['e']) / float(area)), 2)
    stats['j'] = get_globally_greatest_coverage_antenna()

    return stats


def get_global_ant_count():
    global data
    return sum(len(station['ants']) for station in data.get("baseStations"))


def get_global_coverage():
    global data
    single_coverage_pts = []
    multi_coverage_pts = []
    for station in data.get('baseStations'):
        for ant in station.get('ants'):
            for pt in ant.get('pts'):
                current_pt = (pt[0], pt[1])
                if current_pt in multi_coverage_pts:
                    multi_coverage_pts.append(current_pt)
                else:
                    if current_pt in single_coverage_pts:
                        single_coverage_pts.remove(current_pt)
                        multi_coverage_pts.extend([current_pt, current_pt])  # twice to keep track of occurrences
                    else:
                        single_coverage_pts.append(current_pt)
    return single_coverage_pts, multi_coverage_pts


def get_station_stats(bs):
    stats = {'a': int(), 'b': int(), 'c': int(), 'd': int(),
             'e': int(), 'f': float(), 'g': float(), 'h': int()
             }

    (single, multi) = get_station_coverage(bs)

    stats['a'] = len(bs.get('ants'))
    stats['b'] = len(single)
    stats['c'] = len(set(multi))

    stats['d'] = area - stats['b'] - stats['c']

    multi_occurrences = occurrence_dict(multi)

    stats['e'] = (
        (0 if len(single) == 0 else 1) if len(
            multi_occurrences) == 0 else max(
            multi_occurrences.values())
    )
    stats['f'] = get_average_antenna_per_point(single, multi)
    stats['g'] = round(100 * (float(stats['b'] + stats['c']) / float(area)), 2)
    stats['h'] = get_greatest_coverage_antenna(bs)[1]

    return stats


def get_station_coverage(bs):
    ants = bs.get('ants')
    single_coverage_pts = []
    multi_coverage_pts = []

    for ant in ants:
        for pt in ant.get('pts'):
            current_pt = (pt[0], pt[1])
            if current_pt in multi_coverage_pts:
                multi_coverage_pts.append(current_pt)
            else:
                if current_pt in single_coverage_pts:
                    single_coverage_pts.remove(current_pt)
                    multi_coverage_pts.extend([current_pt, current_pt])  # twice to keep track of occurrences
                else:
                    single_coverage_pts.append(current_pt)
    return single_coverage_pts, multi_coverage_pts


def get_global_antenna_stats():
    ant_stats = {'min': 0, 'max': 0, 'avg': float(0)}
    ant_counts = [len(station['ants']) for station in data.get("baseStations")]
    ant_stats['min'] = min(ant_counts)
    ant_stats['max'] = max(ant_counts)
    ant_stats['avg'] = sum(ant_counts) / len(ant_counts)
    return ant_stats


def get_globally_greatest_coverage_antenna():
    max_coverage = 0
    s_id = None
    a_id = None
    for station in data.get('baseStations'):
        for ant in station.get("ants"):
            coverage = len(ant.get("pts"))
            if coverage > max_coverage:
                max_coverage = coverage
                a_id = ant['id']
                s_id = station['id']
    return s_id, a_id


def get_greatest_coverage_antenna(bs):
    max_coverage = 0
    s_id = bs.get('id')
    a_id = None

    for ant in bs.get("ants"):
        coverage = len(ant.get("pts"))
        if coverage > max_coverage:
            max_coverage = coverage
            a_id = ant['id']
    return s_id, a_id


def occurrence_dict(lst):
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    return count_dict


def get_average_antenna_per_point(single, multi):
    temp_sum = len(single)
    multi_occurrences = occurrence_dict(multi)
    for occurrences in multi_occurrences.values():
        temp_sum += occurrences
    return round(temp_sum / (len(single) + len(set(multi))), 2)


def get_global_antennas():
    global data
    return sum(len(station['ants']) for station in data.get("baseStations"))


def option_station_statistics():
    while True:
        choice = show_station_menu().lower()
        if choice == "e":
            print("Exiting to main menu.")
            break
        elif choice == "r":
            show_station_stats(random.choice(data.get("baseStations")))
            break
        elif choice.isdecimal():
            choice = int(choice)
            current_station = next(filter(lambda station: station['id'] == choice, data.get("baseStations")), None)
            if current_station is not None:
                show_station_stats(current_station)
                break
            print("Invalid ID!")
        else:
            print("Invalid input, please try again.")
    return


def show_station_stats(station):
    stats = get_station_stats(station)
    print("Statistics for station", station.get("id"))
    print("Total number of antennas:", stats.get('a'))
    print("Total number of points covered by exactly one antenna:", stats.get('b'))
    print("Total number of points covered by multiple antennas:", stats.get('c'))
    print("Total number of points not covered by any antenna:", stats.get('d'))
    print("Maximum number of antennas covering a single point:", stats.get('e'))
    print("Average number of antennas covering a single point:", stats.get('f'))
    print("Percentage of area covered by the base station:", stats.get('g'), "%")
    print("Antenna with greatest coverage: ID:", stats.get('h'))


def show_station_menu():
    print(textwrap.dedent("""
           ---------Statistics for a single station---------
           Enter the ID of the base station you want the statistics for,
           alternatively enter 'R' or 'E' for the following:
           R. Statistics for a random station
           E. Return to main menu
             """))
    return input("Enter choice: ")


def option_check_coverage():
    print("---------Check Coverage---------")
    while True:
        print("Enter the coordinates of the point you wish to check the coverage for.")

        try:
            lat = float(input("Enter latitude: "))
            lon = float(input("Enter longitude: "))
            covering_stations = check_coverage(lat, lon)
            if not covering_stations:

                print(f"The point at {lat}, {lon} is not covered by the provider.")
                while True:
                    print(textwrap.dedent("""
                        Select an option:
                        1. Locate the closest base station.
                        2. Locate the closest covered point.
                    """))
                    choice = input("Choice: ")
                    if choice == "1":
                        closest_station = find_closest_station([lat, lon])
                        print(f"The nearest base station (ID: {closest_station[3]}) is located at: "
                              f"{closest_station[0]}, {closest_station[1]}.")
                        print(f"Distance: {round(closest_station[2], 4)}")
                        break
                    elif choice == "2":
                        closest_pt_info = find_closest_covered_points([lat, lon])
                        print(
                            f"The nearest covered point is at {closest_pt_info[0][2][0]}, {closest_pt_info[0][2][1]}.")
                        print(f"The point is situated at a distance of {round(closest_pt_info[1], 4)}")
                        print(f"It is covered by Base Station {closest_pt_info[0][0]}, Antenna {closest_pt_info[0][1]}")
                        print(
                            f"The station and antenna are situated at {closest_pt_info[0][3]}, {closest_pt_info[0][4]}")
                        break
                    else:
                        print("Invalid option. Please try again.")
            else:
                print(f"The point at {lat}, {lon} is covered by the following antenna(s):")
                for station in covering_stations:
                    print(f"> Station {station[0]}")
                    for ant in station[1]:
                        print(f"    - Antenna {ant[0]} | Power: {ant[1]}")
                break
            break
        except ValueError:
            print("Please enter valid numbers.")


def find_closest_covered_points(query_pt):
    current_closest_distance = None
    current_closest_pt_info = None
    for station in data.get('baseStations'):
        for ant in station.get('ants'):
            for pt in ant.get('pts'):
                dist = math.dist(query_pt, [float(pt[0]), float(pt[0])])
                if (not current_closest_pt_info) or current_closest_distance > dist:
                    current_closest_pt_info = [station.get('id'), ant.get('id'), pt, station.get('lat'),
                                               station.get('lon')]
                    current_closest_distance = dist

    return [current_closest_pt_info, current_closest_distance]


def find_closest_station(pt):
    current_closest_distance = None
    current_closest_station = None
    for station in data.get('baseStations'):
        dist = math.dist(pt, [float(station.get('lat')), float(station.get('lon'))])
        if (not current_closest_station) or current_closest_distance > dist:
            current_closest_station = station
            current_closest_distance = dist

    return [current_closest_station.get('lat'), current_closest_station.get('lon'), current_closest_distance,
            current_closest_station.get('id')]


def check_coverage(lat, lon):
    covering_stations = []  # format: [(s_id, [(a_id, pow), ...]), ...]
    for station in data.get('baseStations'):
        s_id = station.get('id')
        covering_antennas = []
        for ant in station.get('ants'):
            for pt in ant.get('pts'):
                if pt[0] == lat and pt[1] == lon:
                    covering_antennas.append((ant.get('id'), pt[2]))
                    break
        if covering_antennas:
            covering_stations.append((s_id, covering_antennas))
    return covering_stations


if __name__ == "__main__":
    main()
