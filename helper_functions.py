import math

def distance(point1, point2):
    x_diff = point1[0] - point2[0]
    y_diff = point1[1] - point2[1]

    x_square = x_diff * x_diff
    y_square = y_diff * y_diff

    distance = math.sqrt(x_square + y_square)
    return distance
