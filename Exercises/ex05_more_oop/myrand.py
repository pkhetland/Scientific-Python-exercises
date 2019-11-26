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

    slope = 7 ** 5
    congruence_class = 2 ** 31 - 1

    def __init__(self, seed):
        self._hidden_state = seed

    def rand(self):
        self._hidden_state *= self.slope
        self._hidden_state %= self.congruence_class

        return self._hidden_state

    def random_sequence(self, length):
        """
        Takes length as an argument and uses the class RandIter
        to create a list with n = length random numbers.
        """
        rand_iter = RandIter(self, length)
        randoms = []
        iter(rand_iter)
        for _ in range(length):
            randoms.append(next(rand_iter))
        return randoms

    def infinite_random_sequence(self):
        """
        Generate an infinite sequence of random numbers.

        Yields
        ------
        int
            A random number.
        """
        num_of_randoms = 0
        randoms = []
        while True:
            num_of_randoms += 1
            randoms.append(self.rand())
            yield randoms[num_of_randoms-1]


class RandIter:
    def __init__(self, random_number_generator, length):
        """

        Arguments
        ---------
        random_number_generator :
            A random number generator with a ``rand`` method that
            takes no arguments and returns a random number.
        length : int
            The number of random numbers to generate
        """
        self.generator = random_number_generator
        self.length = length
        self.num_generated_numbers = None

    def __iter__(self):
        """
        Initialise the iterator.

        Returns
        -------
        self : RandIter

        Raises
        ------
        RuntimeError
            If iter is called twice on the same RandIter object.
        """
        if self.num_generated_numbers is None:
            self.num_generated_numbers = 0
            return self
        else:
            raise RuntimeError("__iter__ has already been called on this "
                               "RandIter object.")

    def __next__(self):
        """
        Generate the next random number.

        Returns
        -------
        int
            A random number.

        Raises
        ------
        RuntimeError
            If the ``__next__`` method is called before ``__iter__``.
        StopIteration
            If ``self.length`` random numbers are generated.
        """
        if self.num_generated_numbers is None:
            raise RuntimeError(
                f'{type(self)} is not initialised as an iterator.')
        if self.num_generated_numbers == self.length:
            raise StopIteration
        return self.generator.rand()


if __name__ == "__main__":
    random_number_generator = LCGRand(1)

    print("\nTesting random_sequence function: ")
    for rand in random_number_generator.random_sequence(10):
        print(rand)

    print("\nTesting infinite_random_sequence function: \n")
    for i, rand in enumerate(random_number_generator.infinite_random_sequence()
                             ):
        print(f'The {i}-th random number is {rand}')
        if i > 100:
            break
