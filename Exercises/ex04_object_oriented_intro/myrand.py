# -*- coding: utf-8 -*-

__author__ = 'Petter Hetland'
__email__ = 'pehe@nmbu.no'


class LCGRand:
    """
    This class is a linear congruential generator (LCG),
    which generates numbers according to the following equation


    r[n+1] = a * r[n] mod m

    where ``a = 7**5 = 16807`` and ``m = 2**31-1``.
    """
    def __init__(self, seed):
        self.init_number = seed

    def rand(self):
        next_number = (16807 * self.init_number) % (2**31-1)
        self.init_number = next_number
        return next_number

    def infinite_random_sequence(self):
        """
        Generate an infinite sequence of random numbers.

        Yields
        ------
        int
            A random number.
        """
        pass


class ListRand:
    def __init__(self, list):
        self.list = list
        self.times_called = 0

    def rand(self):
        item = self.times_called
        self.times_called += 1
        if self.times_called <= len(self.list):
            return self.list[item]
        else:
            raise RuntimeError("We're out of numbers!")


if __name__ == '__main__':
    # Print header
    print('\nTesting LCGRand:')
    # Create LCGRand instance:
    lcg_rand = LCGRand(346)
    # Loop through and print the n first random numbers:
    for i in range(5):
        print(f'Random number {i + 1}: {lcg_rand.rand()}')

    # Print header
    print('\nTesting ListRand:')
    # Create ListRand instance:
    list_rand = ListRand([1, 6, 0, 4, 3, 8])
    # Loop through and print the n first random numbers:
    for i in range(8):
        print(f'Random number {i + 1}: {list_rand.rand()}')
