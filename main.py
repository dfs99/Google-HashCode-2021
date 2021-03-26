# read the data.
import os
from State import State
from Street import Street
from Car import Car
from Intersection import Intersection
from copy import deepcopy
import itertools

# global variables for the problem.
time = 0
n_intersections = 0
n_streets = 0
n_cars = 0
scoring_points = 0
all_streets = []
all_cars = []
all_intersections = []


# extracting data.
with open("Data/a_1.txt", "r") as f:
    # first field time for simulation
    # second field nº intersections
    # third field nº streets
    # fourth field nº cars
    # points for each car that achieves its goal
    data = f.readline().split()
    time = int(data[0])
    n_intersections = int(data[1])
    n_streets = int(data[2])
    n_cars = int(data[3])
    scoring_points = int(data[4])

    streets_created = 0
    cars_created = 0
    # create the intersection
    for i in range(0, n_intersections):
        current_intersection = Intersection(i)
        all_intersections.append(current_intersection)

    # while there is still data, loop over it.
    while len(data) > 0:
        data = f.readline().split()

        # creating the graph: vertices - intersections & edges - streets.
        if streets_created < n_streets:
            # set up a street.
            current_steet = Street(data[2], int(data[3]))
            all_streets.append(current_steet)
            streets_created += 1

            # fulfill the intersections
            for intersection in all_intersections:
                # street's intersections coming out
                if intersection.id == int(data[0]):
                    intersection.set_streets_out(current_steet.id)
                # street's intersections coming in
                if intersection.id == int(data[1]):
                    intersection.set_streets_in(current_steet.id)
        # cars
        else:
            if cars_created < n_cars:
                # get the path.
                path = []
                for i in range(1, len(data)):
                    path.append(data[i])
                current_car = Car(path)
                all_cars.append(current_car)
                cars_created += 1


# add all the cars into the current streets.
for s in all_streets:
    for c in all_cars:
        if c.path[0] == s.id:
            # add the car into the street with time ready to leave it.
            c.time_taken_to_cover_a_street = s.time_to_cross
            s.initial_add_car(c)

    #for s in all_streets:
    #    print(s)
    #    print(s.cars)
    #for c in all_cars:
    #    print(c)
for i in all_intersections:
    i.set_light_schedule()


# Algorithm = GBFS is going to be used. Pure Heuristic f(n) = h(n)
def sort_states(state):
    return state.heuristic_value


# HILL CLIMBING WITH GBFS
expanded_state = State(time, all_streets, all_cars, all_intersections)
path = []
while expanded_state.end_state() is False:
    path.append(expanded_state)
    # generate the successors
    children = expanded_state.get_successors()

    if len(children) == 0:
        # no solution has found.
        print("NO SOLUTION FOUND")
        break

    children.sort(key=sort_states)
    expanded_state = children.pop(0)

for o in path:
    print("*"*50)
    print(o)
    print("*" * 50)

