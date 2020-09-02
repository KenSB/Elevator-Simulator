"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator
    max_capacity: The maximum number of people that can board the elevator
    current_floor: The current floor that the elevator is on
    target_floor: The desired floor that the elevator will move to

    === Representation invariants ===
    """
    passengers: List[Person]
    max_capacity: int
    current_floor: int
    target_floor: int

    def __init__(self, max_capacity: int):
        self.passengers = []
        self.current_floor = 1
        self.max_capacity = max_capacity
        ElevatorSprite.__init__(self)

    def fullness(self) -> float:
        """Return the fraction that this elevator is filled.

        The value returned should be a float between 0.0 (completely empty) and
        1.0 (completely full).
        """
        return (len(self.passengers) * 1.0) / self.max_capacity


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting
    complete: A boolean tracking whether or not the person has completed
    their journey
    === Representation invariants ===
    start >= 1
    target >= 1
    wait_time >= 0
    """
    start: int
    target: int
    wait_time: int
    complete: bool

    def __init__(self, start_floor: int, target_floor: int):
        self.start = start_floor
        self.target = target_floor
        self.wait_time = 0
        PersonSprite.__init__(self)
        self.complete = False

    def get_anger_level(self) -> int:
        """Return this person's anger level.

        A person's anger level is based on how long they have been waiting
        before reaching their target floor.
            - Level 0: waiting 0-2 rounds
            - Level 1: waiting 3-4 rounds
            - Level 2: waiting 5-6 rounds
            - Level 3: waiting 7-8 rounds
            - Level 4: waiting >= 9 rounds

        >>> jim = Person(1,5)
        >>> jim.increase_wait_time()
        >>> jim.increase_wait_time()
        >>> jim.increase_wait_time()
        >>> jim.increase_wait_time()
        >>> jim.get_anger_level()
        1
        >>> bob = Person(1,5)
        >>> bob.increase_wait_time()
        >>> bob.increase_wait_time()
        >>> bob.complete = True
        >>> bob.increase_wait_time()
        >>> bob.increase_wait_time()
        >>> bob.get_anger_level()
        0
        >>> Person(1,5).get_anger_level()
        0
        >>> bill = Person(2,3)
        >>> bill.wait_time = 100
        >>> bill.get_anger_level()
        4
        """
        if self.wait_time < 3:
            return 0
        elif self.wait_time < 5:
            return 1
        elif self.wait_time < 7:
            return 2
        elif self.wait_time < 9:
            return 3
        else:
            return 4

    def increase_wait_time(self) -> None:
        """Increases the wait time of the person by 1 for every round that
        they are not yet at their destination.
        >>> david = Person(1,3)
        >>> david.complete = True
        >>> david.increase_wait_time()
        >>> david.wait_time
        0
        """
        if not self.complete:
            self.wait_time += 1


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4
    })
