import textwrap
import reading
import random

data = reading.read_file("test.json")
stations = data.get("baseStations")
area = round(((abs(data.get('max_lat') - data.get('min_lat')) + data.get('step')) / data.get('step')) * (
        (abs(data.get('max_lon') - data.get('min_lon')) + data.get('step')) / data.get('step')))
station_ids = []
ant_count = 0
ant_stats = {'min': 0, 'max': 0, 'avg': float(0)}
point_stats = {'single_coverage': set(), 'multi_coverage': [], 'coverage_count': 0, 'total_points': 0,
               'average_antenna_count': float(),
               'percentage_covered': float(), 'greatest_coverage_id': (0, 0)}


def main():
    while True:
        choice = show_main_menu()
        match choice:
            case "1":
                show_global_statistics()
            case "2":
                option_station_statistics()
            case "3":
                print("Check Coverage")
            case "4":
                print("Exiting")
                reading.read_file("test.json")
                break
            case _:
                print("Invalid choice")
    return


def show_main_menu():
    print(textwrap.dedent("""
        1. Display Global Statistics
        2. Display Base Station Statistics
        3. Check Coverage
        4. Exit
          """))
    return input("Enter choice: ")


def show_global_statistics():
    print("Total number of base stations:", len(data.get("baseStations")))  # a
    print("Total number of antennas:", ant_count)  # b
    print(
        f"Max, min, and average antenna count per base station: "
        f"{ant_stats['max']}, {ant_stats['min']}, {ant_stats['avg']}")  # c
    print("Total number of points covered by a single antenna:",
          len(point_stats.get('single_coverage')))  # d
    print("Total number of points covered by multiple antennas:",
          len(set(point_stats.get('multi_coverage'))))  # e
    print("Total number of squares not covered by any antenna:", (point_stats['total_points']
                                                                  - len(point_stats.get('single_coverage')) - len(
                set(point_stats.get('multi_coverage')))))  # f
    print("Maximum number of antennas covering a single point:",
          ((0 if len(point_stats['single_coverage']) == 0 else 1) if len(
              point_stats['multi_coverage']) == 0 else max(
              occurrence_dict(point_stats['multi_coverage']).values())))  # g
    print("Average number of antennas covering a single point:", point_stats['average_antenna_count'])  # h
    print(
        f"Percentage of area covered by the provider: "
        f"{round(100 * float(point_stats['coverage_count']) / float(point_stats['total_points']), 2)}%")  # i
    print("Antenna with greatest coverage:", get_greatest_coverage_antenna())  # j
    return


def get_global_stats():
    stats = {'a': int(), 'b': int(), 'c': (int(), int(), int()),
             'd': int(), 'e': int(), 'f': int(), 'g': int(),
             'h': float(), 'i': float(), 'j': int()
             }

    stats['a'] = len(data.get("baseStations"))
    stats['b'] = get_global_ant_count()
    ant_stats = get_global_antenna_stats()
    stats['c'] = (ant_stats['max'], ant_stats['min'], ant_stats['avg'])


    return stats


def get_global_ant_count():
    global data
    return sum(len(station['ants']) for station in data.get("baseStations"))

def get_global_coverage():
    global data
    for station in data.get('baseStations'):
        for ()

def get_station_stats(bs):
    global area
    ants = bs.get('ants')

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
    covered_point_count = stats['b'] + stats['c']
    stats['g'] = round(100 * float(covered_point_count / float(area)), 2)
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


def get_global_point_stats():
    generate_covered_points()
    # get_total_points()
    # get_average_antenna_per_point()


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


def generate_covered_points():
    global point_stats
    single_coverage_points = set()
    multi_coverage_points = []
    for station in data.get("baseStations"):
        for ant in station.get("ants"):

            for point in ant.get("pts"):
                current_pt = (point[0], point[1])

                if current_pt in multi_coverage_points:
                    multi_coverage_points.append(current_pt)
                else:
                    if current_pt in single_coverage_points:
                        single_coverage_points.remove(current_pt)
                        multi_coverage_points.extend([current_pt, current_pt])  # twice to keep track of occurrences
                    else:
                        single_coverage_points.add(current_pt)
    point_stats['single_coverage'] = single_coverage_points
    point_stats['multi_coverage'] = multi_coverage_points
    point_stats['coverage_count'] = len(single_coverage_points) + len(set(multi_coverage_points))


def get_total_points():
    global data
    global point_stats
    x1 = data.get('min_lat')
    x2 = data.get('max_lat')
    y1 = data.get('min_lon')
    y2 = data.get('max_lon')
    step = data.get('step')
    point_stats['total_points'] = round(((abs(x2 - x1) + step) / step) * ((abs(y2 - y1) + step) / step))


def occurrence_dict(lst):
    count_dict = {}
    for item in lst:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1

    return count_dict


def get_average_antenna_per_point(single, multi):  # i'm sorry about these names
    temp_sum = len(single)
    multi_occurrences = occurrence_dict(multi)
    for occurrences in multi_occurrences.values():
        temp_sum += occurrences
    return temp_sum / (len(single) + len(set(multi)))


def generate_id_list():
    global station_ids
    station_ids = [station['id'] for station in data.get("baseStations")]


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
            show_station_statistics(random.choice(station_ids))
            break
        elif choice.isdecimal():
            choice = int(choice)
            current_station = next(filter(lambda station: station['id'] == choice, data.get("baseStations")), None)
            if current_station is not None:
                show_station_statistics(current_station)
                break
            print("Invalid ID!")
        else:
            print("Invalid input, please try again.")
    return


def show_station_statistics(station):
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
    print("Check Coverage")
    return


if __name__ == "__main__":
    main()
