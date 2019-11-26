# -*- coding: utf-8 -*-

__author__ = 'Petter Hetland'
__email__ = 'pehe@nmbu.no'

import random as r


class Walker:
    def __init__(self, start, home):
        self.x = start
        self.h = home
        self.num_steps = 0

    def move(self):
        if r.randint(0, 1) > 0.5:
            self.x += 1
        else:
            self.x -= 1

        self.num_steps += 1

    def get_position(self):
        return self.x

    def is_at_home(self):
        if self.x == self.h:
            return True
        return False

    def get_steps(self):
        return self.num_steps


class Simulation():
    def __init__(self, start, home, seed):
        """Initialise the simulation

        Arguments
        --------
        start : int
            The walker's initial position
        home : int
            The walk ends when the walker reaches home
        seed : int
            Random number generator"""
        self.start = start
        self.home = home
        self.seed = seed

    def single_walk(self):
        """Simulate single walk from start to home, returning number of steps.

        Returns
        --------
        int
            The number of steps taken
        """
        w = Walker(self.start, self.home)

        while not w.is_at_home():
            w.move()

        return w.get_steps()

    def run_simulation(self, num_walks):
        """
        Run a set of walks, returns lsit fo number of steps taken.

        Arguments
        ---------
        num_walks : int
            The number of walks to simulate

        Returns
        --------
        list[int]
            List with the number of steps per walk
        """
        r.seed(self.seed)

        moves_count = [self.single_walk() for _ in range(num_walks)]

        return moves_count


if __name__ == '__main__':
    # Simulation number one:
    sim_one = Simulation(0, 10, 12345)

    # Header for sim one and two:
    print(f"""
The result of 20 simulations with start at {sim_one.start}, \
home at {sim_one.home} and a seed of {sim_one.seed} is:
    """)

    print(sim_one.run_simulation(20))

    # Simulation number two:
    sim_two = Simulation(0, 10, 12345)

    print(sim_two.run_simulation(20))

    # Simulation number three:
    sim_three = Simulation(0, 10, 54321)

    # Header for simulation number three:
    print(f"""
The result of 20 simulations with start at {sim_three.start}, \
home at {sim_three.home} and a seed of {sim_three.seed} is:
    """)

    print(sim_three.run_simulation(20))

    # Simulation number four:
    sim_four = Simulation(10, 0, 12345)

    # Header for simulation number four and five:
    print(f"""
The result of 20 simulations with start at {sim_four.start}, \
home at {sim_four.home} and a seed of {sim_four.seed} is:
        """)

    print(sim_four.run_simulation(20))

    # Simulation number five:
    sim_five = Simulation(10, 0, 12345)

    print(sim_five.run_simulation(20))

    # Simulation number six:
    sim_six = Simulation(10, 0, 54321)

    # Header for simulation number six:
    print(f"""
The result of 20 simulations with start at {sim_six.start}, \
home at {sim_six.home} and a seed of {sim_six.seed} is:
        """)

    print(sim_six.run_simulation(20))
