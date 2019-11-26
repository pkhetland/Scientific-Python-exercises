# -*- coding: utf-8 -*-

__author__ = 'Petter Hetland'
__email__ = 'pehe@nmbu.no'

import random as r


class Walker:
    def __init__(self, x_0, h):
        self.x = x_0
        self.h = h
        self.num_steps = 0

    def move(self):
        if r.randint(0, 1) > 0.5:
            self.x += 1
        else:
            self.x -= 1

        self.num_steps += 1
        return self.x, self.num_steps

    def get_position(self):
        return self.x

    def is_at_home(self):
        return self.x == self.h

    def get_steps(self):
        return self.num_steps


def walk_home(initial_position, distance):
    """Runs a full simulation of getting from the initial position
    to home, with a given distance beetween.
    """
    w = Walker(initial_position, distance)
    while not w.is_at_home():
        w.move()
    return w.get_steps()


if __name__ == '__main__':
    """Test walk_home() function from walker.py with different distances
    """

    print('\nTesting walk_home function:')

    for distance in [1, 2, 5, 10, 20, 50, 100]:
        # Loops through given distances
        moves_count = [walk_home(0, distance) for _ in range(5)]
        # List captures result of n number of simulations
        print("Distance: {:5} -> Path lengths: {}"
              .format(distance, moves_count))
        # Prints result
