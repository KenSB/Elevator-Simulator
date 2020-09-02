"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional
from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """
    tom: Person

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

               Preconditions:
                   max_floor >= 2
                   num_people is None or num_people >= 0
               """
        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        Generates a fixed number of people each round with random starting
        and ending position

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        newcomers = {}
        existing_floors = []
        count = 0
        while not count == self.num_people:
            rand1 = random.randint(1, self.max_floor)
            if count == 0:
                newcomers[rand1] = []
                existing_floors.append(rand1)
            elif rand1 not in existing_floors:
                newcomers[rand1] = []
                existing_floors.append(rand1)
            rand2 = random.randint(1, self.max_floor)
            while rand1 == rand2:
                rand2 = random.randint(1, self.max_floor)
            newcomers[rand1].append(Person(rand1, rand2))
            count += 1
        return newcomers


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.
    """
    rounds: Dict[int, List[int]]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        self.rounds = {}
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                ints = []
                for char in line:
                    ints.append(int(char.strip()))
                self.rounds[ints.pop(0)] = ints

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        Generates new arrivals based on a csv file.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        newcomers = {}
        keys = self.rounds.keys()
        if round_num in keys:
            while not len(self.rounds[round_num]) == 0:
                # print(len(self.rounds[round_num]))
                hold1 = self.rounds[round_num].pop(0)
                hold2 = self.rounds[round_num].pop(0)
                print(hold1)
                print(hold2)
                if hold1 in newcomers.keys():
                    newcomers[hold1].append(Person(hold1, hold2))
                else:
                    newcomers[hold1] = [Person(hold1, hold2)]
            return newcomers
        else:
            newcomers[round_num] = []
            return newcomers


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        This method generates directions randomly.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        directions = []
        for elevator in elevators:
            rand = random.randint(1, 2)
            if elevator.current_floor == 1:
                if rand == 1:
                    directions += [Direction.UP]
                    elevator.current_floor += 1
                else:
                    directions += [Direction.STAY]
            elif elevator.current_floor == max_floor:
                if rand == 1:
                    directions += [Direction.DOWN]
                    elevator.current_floor -= 1
                else:
                    directions += [Direction.STAY]
            else:
                rand = random.randint(1, 3)
                if rand == 1:
                    directions += [Direction.UP]
                    elevator.current_floor += 1
                elif rand == 2:
                    directions += [Direction.STAY]
                else:
                    directions += [Direction.DOWN]
                    elevator.current_floor -= 1
        return directions


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def choose_direction(self, elevators: List[Elevator]) -> List[Direction]:
        """Return a list of directions based on the target floor
        of each elevator.

        Precondition: the target floor must exist
        """
        directions = []
        for elevator in elevators:
            if elevator.target_floor == 0 or \
                    elevator.current_floor == elevator.target_floor:
                directions.append(Direction.STAY)
            elif elevator.current_floor < elevator.target_floor:
                directions.append(Direction.UP)
                elevator.current_floor += 1
            else:
                directions.append(Direction.DOWN)
                elevator.current_floor -= 1
        return directions

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        This method generates directions based on the PushyPassenger rules
        provided

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        keys = waiting.keys()
        floors_with_people = []
        for key in keys:
            if not waiting[key] == []:
                floors_with_people.append(key)

        for elevator in elevators:
            elevator.target_floor = 0
            if len(elevator.passengers) == 0:
                if not floors_with_people == []:
                    floor = 1
                    while elevator.target_floor == 0:
                        if floor in floors_with_people:
                            elevator.target_floor = floor
                        else:
                            floor += 1
            else:
                elevator.target_floor = elevator.passengers[0].target
        return self.choose_direction(elevators)


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def choose_direction(self, elevators: List[Elevator]) -> List[Direction]:
        """Return a list of directions based on the target floor
        of each elevator.

        Precondition: the target floor must exist

        """
        directions = []
        for elevator in elevators:
            if elevator.target_floor == 0 or \
                    elevator.current_floor == elevator.target_floor:
                directions.append(Direction.STAY)
            elif elevator.current_floor < elevator.target_floor:
                directions.append(Direction.UP)
                elevator.current_floor += 1
            else:
                directions.append(Direction.DOWN)
                elevator.current_floor -= 1
        return directions

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        This method generates directions based on the ShortSighted rules
        provided

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        keys = waiting.keys()
        floors_with_people = []
        for key in keys:
            if not waiting[key] == []:
                floors_with_people.append(key)
        for elevator in elevators:
            elevator.target_floor = 0
            if len(elevator.passengers) == 0:
                if not floors_with_people == []:
                    add = 1
                    while elevator.target_floor == 0:
                        if (elevator.current_floor - add) in floors_with_people:
                            elevator.target_floor = elevator.current_floor - add
                        elif(elevator.current_floor + add) in floors_with_people:
                            elevator.target_floor = elevator.current_floor + add
                        else:
                            add += 1
                else:
                    elevator.target_floor = elevator.current_floor
            else:
                new_target = 0
                distance = 6
                for passenger in elevator.passengers:
                    test = passenger.target - elevator.current_floor
                    if test < 0:
                        if (test * -1) < distance:
                            new_target = passenger.target
                            distance = test * -1
                        elif (test * -1) == distance:
                            new_target = passenger.target
                            distance = test * -1
                    else:
                        if test < distance:
                            new_target = passenger.target
                            distance = test
                elevator.target_floor = new_target
        return self.choose_direction(elevators)


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201']
    })
