# -*- coding: utf-8 -*-

__author__ = 'Petter Hetland'
__email__ = 'pehe@nmbu.no'

import random as r
from walker_sim import Walker, Simulation


class BoundedWalker(Walker):
    def __init__(self, start, home, left_limit, right_limit):
        """
        Initialise the walker

        Arguments
        ---------
        start : int
            The walker's initial position
        home : int
            The walk ends when the walker reaches home
        left_limit : int
            The left boundary of walker movement
        right_limit : int
            The right boundary  of walker movement
        """
        super().__init__(start, home)

        self.left_limit = left_limit
        self.right_limit = right_limit

    def bounded_move(self):
        if r.randint(0, 1) > 0.5:
            if not self.x >= self.right_limit:
                self.x += 1
                self.num_steps += 1
            else:
                self.num_steps += 1
        else:
            if self.x > self.left_limit:
                self.x -= 1
                self.num_steps += 1
            else:
                self.num_steps


class BoundedSimulation(Simulation):
    def __init__(self, start, home, seed, left_limit, right_limit):
        """
        Initialise the simulation

        Arguments
        ---------
        start : int
            The walker's initial position
        home : int
            The walk ends when the walker reaches home
        seed : int
            Random generator seed
        left_limit : int
            The left boundary of walker movement
        right_limit : int
            The right boundary  of walker movement
        """
        super().__init__(start, home, seed)

        self.left_limit = left_limit
        self.right_limit = right_limit

    def bounded_walk(self):
        """Simulate single walk from start to home, returning number of steps.

        Returns
        --------
        int
            The number of steps taken
        """
        bw = BoundedWalker(self.start,
                           self.home,
                           self.left_limit,
                           self.right_limit)

        while not bw.is_at_home():
            bw.bounded_move()

        return bw.get_steps()

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

        moves_count = [self.bounded_walk() for _ in range(num_walks)]

        return moves_count


if __name__ == '__main__':
    for l_limit in [0, -10, -100, -1000, -10000]:
        bounded_sim = BoundedSimulation(0, 20, 2, l_limit, 20)
        print('With a left boundary for {:6}: '.format(l_limit),
              bounded_sim.run_simulation(20))
