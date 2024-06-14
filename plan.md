# the plan
## 1
a. The total number of base stations for the provider
b. The total number of antennas
c. The maximum, minimum and average number of antennas per base station
d. The total number of squares (points) in the area that are covered by exactly one antenna.
e. The total number of squares (points) in the area that are covered by more than one 
antenna.
f. The total number of squares (points) in the area that are not covered by any antenna.
g. The maximum number of antennas that cover one square (point).
h. The average number of antennas covering a square (point).
i. The percentage of the covered area by the provider 
(points_covered_by_at_least_one_antenna/total_number_of_points_in_the_area)
j. The id of the antenna and base station covering the maximum number of squares
(points)

## 2
a. The total number of antennas
b. The total number of points covered by exactly one antenna.
c. The total number of points covered by more than one antenna.
d. The total number of points not covered by any antenna.
e. The maximum number of antennas that cover one point.
f. The average number of antennas covering a point.
g. The percentage of the covered area by the base station (similar to the global statistics).
h. The id of the antenna that covers the maximum number of points.

## 3
- user enters lat and lon (not necesarily in JSON)
- check if point is covered, return all base stations and antennas covering it with respective powers

Assume:

global 


class BaseStation:

    def __init__(self, id, lat, lon, ants):
        self.id = id
        self.lat = lat
        self.lon = lon
        self.ants = ants
    
    get_antenna_count


class Antenna:
    might need bs_id

    def __init__(self, id, frq, bw, pts):
        self.id = id
        self.frq = frq
        self.bw = bw
        self.pts = pts

class Point: 
    
    def __init__(self, lat, lon, pow):
        self.lat = lat
        self.lon = lon
        self.pow = pow