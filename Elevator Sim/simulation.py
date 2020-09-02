"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    completed: a list of people who have completed their journey
    num_rounds:
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]
    completed: List[Person]
    num_rounds: int

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        self.arrival_generator = config["arrival_generator"]
        self.moving_algorithm = config["moving_algorithm"]
        self.elevators = []
        count = 0
        while not count == config["num_elevators"]:
            self.elevators.append(Elevator(config["elevator_capacity"]))
            count += 1
        self.num_floors = config["num_floors"]
        count2 = 0
        self.waiting = {}
        while not count2 == config["num_floors"]:
            self.waiting[count2 + 1] = []
            count2 += 1
        self.completed = []
        self.num_rounds = 0

        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.
        self.visualizer = Visualizer(self.elevators
                                     , self.num_floors
                                     , config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.num_rounds += 1

            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            for elevator in self.elevators:
                for person in elevator.passengers:
                    person.increase_wait_time()

            for floor in self.waiting:
                for person in self.waiting[floor]:
                    person.increase_wait_time()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""
        new_people = self.arrival_generator.generate(round_num)
        for _, people in new_people.items():
            if not people == []:
                for floor in new_people:
                    count = 0
                    while not count == len(new_people[floor]):
                        self.waiting[floor] = [new_people[floor].pop()] + \
                                          self.waiting[floor]
                self.visualizer.show_arrivals(self.waiting)
            else:
                return None

    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""
        count = 0
        for elevator in self.elevators:
            for person in elevator.passengers:
                count += 1
                if person.target == elevator.current_floor:
                    self.visualizer.show_disembarking(person, elevator)
                    elevator.passengers.remove(person)
                    self.completed.append(person)

    def _handle_boarding(self) -> None:
        """Handle boarding of people and visualize."""
        for elevator in self.elevators:
            while not len(self.waiting.get(elevator.current_floor)) == 0 and \
                    not len(elevator.passengers) == elevator.max_capacity:
                person = self.waiting.get(elevator.current_floor).pop()
                self.visualizer.show_boarding(person, elevator)
                elevator.passengers += [person]

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.
        Use this simulation's moving algorithm to move the elevators.
        """
        moves = self.moving_algorithm.move_elevators(self.elevators,
                                                     self.waiting,
                                                     self.num_floors)
        self.visualizer.show_elevator_moves(self.elevators, moves)

    ############################################################################
    # Statistics calculations
    ############################################################################

    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        total_people = 0
        sum_wait_time = 0
        max_wait = 0
        min_wait = self.num_rounds
        for floor in self.waiting:
            total_people += len(self.waiting[floor])

        for elevator in self.elevators:
            total_people += len(elevator.passengers)

        for person in self.completed:
            sum_wait_time += person.wait_time
            if min_wait > person.wait_time:
                min_wait = person.wait_time
            if max_wait < person.wait_time:
                max_wait = person.wait_time
        total_people += len(self.completed)
        avg_time = sum_wait_time / len(self.completed)
        print(f'{min_wait}  {avg_time}  {max_wait}')
        return {
            'num_iterations': self.num_rounds,
            'total_people': total_people,
            'people_completed': len(self.completed),
            'max_time': max_wait,
            'min_time': min_wait,
            'avg_time': avg_time
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 5,
        'num_elevators': 2,
        'elevator_capacity': 1,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': algorithms.FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': algorithms.ShortSighted(),
        # Note that we aren't visualizing anything here.
        # Your code should still work properly (and run a lot faster) with this
        # set to False.
        'visualize': True
    }
    sim = Simulation(config)
    num_rounds = 10
    results = sim.run(num_rounds)
    return results


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
    #     'max-nested-blocks': 4
    # })
    print(sample_run())
