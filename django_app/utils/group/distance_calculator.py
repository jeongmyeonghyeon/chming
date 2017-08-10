from math import sin, cos, sqrt, atan2, radians


def distance_calculator(origin_lat, origin_lng, target_lat, target_lng):
    R = 6373.0

    origin_lat = radians(origin_lat)
    origin_lng = radians(origin_lng)
    target_lat = radians(target_lat)
    target_lng = radians(target_lng)

    dlon = target_lng - origin_lng
    dlat = target_lat - origin_lat

    a = sin(dlat / 2) ** 2 + cos(origin_lat) * cos(target_lat) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
