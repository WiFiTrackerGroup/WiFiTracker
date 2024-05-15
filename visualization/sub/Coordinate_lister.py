from config import *
import pickle
import os
from shapely.geometry import Point, Polygon

def int_coord(poly):
    minx, miny, maxx, maxy = map(int, poly.bounds)
    points = [(x,y) for x in range(minx, maxx+1) for y in range(miny, maxy+1) if Point(x,y).within(poly)]
    return points

def main():
    choice = "Even"

    current_rooms = ROOMS[choice]["room_list"]

    coord_dict = {}

    for r in list(current_rooms.keys()):
        x = current_rooms[r]["X"]
        y = current_rooms[r]["Y"]
        poly = Polygon(zip(x, y))
        internal = int_coord(poly)
        coord_dict[r] = internal

    file_name = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(file_name, "Image", choice + ".pkl")
    
    with open(file_name, 'wb') as file:
        pickle.dump(coord_dict, file)

if __name__ == "__main__":
    main()