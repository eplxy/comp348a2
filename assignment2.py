import textwrap
import reading
import random

data = reading.read_file("test.json")

valid_ids = []
ant_count = 0
ant_stats = {'min': 0, 'max': 0, 'avg': float(0)}
point_stats = {'single_coverage': set(), 'multi_coverage': [], 'coverage_count': 0, 'total_points': 0,
               'average_antenna_count': float(),
               'percentage_covered': float(), 'greatest_coverage_id': (0, 0)}


def main():
    extract_data()
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


def extract_data():
    global data
    data = reading.read_file("test.json")
    generate_id_list()
    count_global_antennas()
    get_global_antenna_stats()
    get_global_point_stats()

    return


def get_global_antenna_stats():
    global ant_stats
    ant_counts = [len(station['ants']) for station in data.get("baseStations")]
    ant_stats['min'] = min(ant_counts)
    ant_stats['max'] = max(ant_counts)
    ant_stats['avg'] = sum(ant_counts) / len(ant_counts)


def get_global_point_stats():
    generate_covered_points()
    get_total_points()
    get_average_antenna_per_point()


def get_greatest_coverage_antenna():
    max_coverage = 0
    s_id = None
    a_id = None

    for station in data.get("baseStations"):
        for ant in station.get("ants"):
            coverage = len(ant.get("pts"))
            if coverage > max_coverage:
                max_coverage = coverage
                s_id = station['id']
                a_id = ant['id']

    return "baseStation: " + str(s_id) + ", antenna: " + str(a_id)


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


def get_average_antenna_per_point():  # i'm sorry about these names
    temp_sum = len(point_stats['single_coverage'])
    for occurrences in occurrence_dict(point_stats['multi_coverage']).values():
        temp_sum += occurrences
    point_stats['average_antenna_count'] = temp_sum / point_stats['coverage_count']


def generate_id_list():
    global valid_ids
    valid_ids = [station['id'] for station in data.get("baseStations")]


def count_global_antennas():
    global ant_count
    ant_count = sum(len(station['ants']) for station in data.get("baseStations"))


def option_station_statistics():
    while True:
        choice = show_station_menu().lower()
        if choice == "e":
            print("Exiting to main menu.")
            break
        elif choice == "r":
            show_station_statistics(random.choice(valid_ids))
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
    return


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
