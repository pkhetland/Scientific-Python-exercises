# -*- coding: utf-8 -*-

__author__ = "Eirik Helland, Petter Hetland"
__email__ = "eihelland@nmbu.no, pehe@nmbu.no"


import random
import statistics as s


def add_players(n):
    """
    Add_players(n) makes a list of lists containing 0. Each list of 0
    represents a player and n is the number of players in the game.
    This will be used to store where the players are on the board
    and track their history using append.
    """
    player_position_list = [[0] for _ in range(n)]
    return player_position_list


def snake_and_ladders():
    """
    Snake_and_ladders() makes a dictionary which contains all the positions
     on the board with ladders or snakes. This will be used to promote
     or relegate a player to the intended position.
    """
    snake_and_ladders_dict = {
        1: 40,
        8: 10,
        36: 52,
        43: 62,
        49: 79,
        65: 82,
        68: 85,
        24: 5,
        33: 3,
        42: 30,
        56: 37,
        64: 27,
        74: 12,
        87: 70,
    }
    return snake_and_ladders_dict


def dice_roll():
    """Dice_roll() tosses a 6-sided roll_value and returns the value.
    """
    roll_value = random.randint(1, 6)
    return roll_value


def single_game(num_players):
    """
    Returns duration of single game.

    Arguments
    ---------
    num_players : int
        Number of players in the game

    Returns
    -------
    num_moves : int
        Number of moves the winning player needed to reach the goal
    """
    positions = add_players(num_players)
    snake_ladders = snake_and_ladders()
    winner = []
    has_won = False
    while has_won is not True:  # Runs loop until win-state
        for player in range(num_players):
            dice = dice_roll()
            positions[player].append(positions[player][-1] + dice)
            if positions[player][-1] in snake_ladders.keys():
                positions[player][-1] = snake_ladders[positions[player][-1]]
            else:
                pass
            if positions[player][-1] >= 90:
                winner = positions[player]
                has_won = True  # Loop is exited
            else:
                pass
    return len(winner) - 1


def multiple_games(num_games, num_players):
    """
    Returns durations of a number of games.

    Arguments
    ---------
    num_games : int
        Number of games to play
    num_players : int
        Number of players in the game

    Returns
    -------
    num_moves : list
        List with the numbedr of moves needed in each game.
    """
    num_moves = []
    for _ in range(num_games):
        num_moves.append(single_game(num_players))
    return num_moves


def multi_game_experiment(num_games, num_players, seed):
    """Returns durations of a number of games when playing with given seed.

    Arguments
    ---------
    num_games : int
        Number of games to play
    num_players : int
        Number of players in the game
    seed : int
        Seed used to initialise the random number generator

    Returns
    -------
    num_moves : list
        List with the numbedr of moves needed in each game.
    """
    random.seed(seed)
    num_moves = []
    for _ in range(num_games):
        num_moves.append(single_game(num_players))
    return num_moves


if __name__ == "__main__":
    """
    Main block runs an experiment of 100 games with 4 players and
    a seed of 10.
    
    Returns
    -------
    - Minimum number (int) of moves among the 100 games run
    - Maximum number (int) of moves among the 100 games run
    - Mean value (float) of all game durations
    - Median value (float) of all game durations
    """

    experiment = multi_game_experiment(100, 4, 10)

    print(f"Minimum number of moves: {min(experiment)}")
    print(f"Maximum number of moves: {max(experiment)}")
    print(f"Mean value of the experiment: {s.mean(experiment)}")
    print(f"Median value of the experiment: {s.median(experiment)}")
