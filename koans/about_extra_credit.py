#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from random import randint
from runner.koan import *
from koans.about_dice_project import DiceSet
from koans.about_scoring_project import score

def make_table(headers=[], rows=[]):
    """
        Returns a string that when printed looks like:

        -----------------------------------------
        | Header 1      | Header 2        | ... |
        |---------------|-----------------|-----|
        | Row 1 Col 1   | Row 1 Col 2     | ... |
        | .             | .               | ... |
        | .             | .               | ... |
        | .             | .               | ... |
        | Row 200 Col 1 | Row 200 Col 2   | ... |
        -----------------------------------------
    """
    def make_row(row, col_lengths):
        padded_values = [
            f" {row[i]}{' ' * (col_lengths[i] - len(str(row[i])) - 2)} "
            for i in range(len(col_lengths))
        ]
        return "|" + "|".join(padded_values) + "|"

    col_lengths = [
        max(len(headers[i]), *[len(str(row[i])) for row in rows]) + 2
        for i in range(len(headers))
    ]

    lines = []

    lines.append(f"-{'-'.join(['-' * l for l in col_lengths])}-")

    if len(headers) > 0:
        lines.append(make_row(headers, col_lengths))

    lines.append(f"|{'|'.join(['-' * col_length for col_length in col_lengths])}|")

    if (len(rows) > 0):
        [lines.append(make_row(row, col_lengths)) for row in rows]

    lines.append(f"-{'-'.join(['-' * col_length for col_length in col_lengths])}-")

    return '\n'.join(lines)

def prompt_for_input(sentence, allowed_inputs):
    while True:
        given_input = input(sentence)
        if given_input in allowed_inputs:
            return given_input
        else:
            print(f"Please enter one of {allowed_inputs}")

class Player():
    def __init__(self, name):
        self._name = name
        self._score = 0

        # must score 300 points in a single turn before scoring unlocked
        self._scoring_unlocked = False

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    def play_turn(self, dice_set):
        score_for_turn = 0
        num_die_available_for_throw = 5

        print(f"It is now Player {self.name}'s turn. Their score so far is {self.score}.")
        print("")

        while True:
            should_throw = prompt_for_input(
                f"Player {self.name} has accumulated {score_for_turn} points this turn, and holds {num_die_available_for_throw} die. Throw? (Y/n) ",
                ['y', 'Y', 'n', 'N', '']
            )
            if should_throw not in ['y', 'Y', '']:
                print("")
                break

            throw = dice_set.roll(num_die_available_for_throw)
            score_for_throw, num_nonscoring_die = score(
                throw, return_num_nonscoring_die=True)
            print(f"Player {self.name} has thrown {throw}")

            if score_for_throw == 0:
                score_for_turn = 0
                print(f"Player {self.name}'s throw is worth 0 points. They lose their turn, and all points accumulated this turn!")
                break

            print(f"Player {self.name}'s throw is worth {score_for_throw} points.")

            if num_nonscoring_die == 0:
                num_die_available_for_throw = 5
                print(f"Since there were no non-scoring die this throw, player {self.name} can choose to throw again with all {num_die_available_for_throw} die.")
            else:
                num_die_available_for_throw = num_nonscoring_die
                print(f"Since there were {num_nonscoring_die} non-scoring die this throw, player {self.name} can choose to throw again.")

            print("")
            score_for_turn += score_for_throw

        print(f"Player {self.name} has ended their turn with a score of {score_for_turn}")

        if not self._scoring_unlocked and score_for_turn >= 300:
            self._scoring_unlocked = True
            print(f"By scoring more than 300 in a single turn, player {self.name} has unlocked scoring")

        if self._scoring_unlocked:
            new_score = self._score + score_for_turn
            print(f"Player {self.name}'s score is now {new_score} ({self.score} + {score_for_turn}).")
            self._score = new_score
        elif score_for_turn > 0:
            print(f"Since they have not yet unlocked scoring, player {self.name}'s total score is still 0")

        print("")

class Game():
    def __init__(self):
        self._players = None
        self._dice_set = DiceSet()

    def start(self):
        print("Welcome to GREED. Read 'GREEDS_RULES.txt' to understand the rules.")
        print("")

        # body of this loop represents a single game
        while True:
            n_players = self._prompt_num_players()
            self._players = [Player(str(i + 1)) for i in range(n_players)]

            # keep throwing for each player until one player reaches a score of 3000
            next_player_idx = 0
            while True:
                cur_player = self._players[next_player_idx]
                cur_player.play_turn(self._dice_set)
                next_player_idx = (next_player_idx + 1) % len(self._players)
                if (cur_player.score >= 3000):
                    print(f"Player {cur_player.name} is the first to reach a score of 3000!")
                    print(f"The remaining players will now get one last turn.")
                    break

            # let all other players get one more turn
            leading_player_idx = (n_players - 1) if next_player_idx == 0 else (next_player_idx - 1)
            [self._players[i].play_turn(self._dice_set) for i in range(leading_player_idx + 1, n_players)]
            [self._players[i].play_turn(self._dice_set) for i in range(leading_player_idx)]

            # compare scores and declare winner
            self._declare_winner()

            # ask if want to play again
            if not self._prompt_play_again():
                break

        print("\nThank you for playing GREED\n")


    def _prompt_num_players(self):
        n = None
        while not (n.__class__ == int and n >= 2):
            try:
                n = int(input("How many players want to play? "))
                if n < 2: raise ValueError
            except ValueError:
                print("Error: Please enter a whole number greater than 1.\n")
        print("")
        return n

    def _declare_winner(self):
        """
            Prints a table that looks like:
            ----------------------
            | Player     | Score |
            |------------|-------|
            | 1          | 1000  |
            | 2 (WINNER) | 3000  |
            ----------------------
        """
        max_score = max(*[player.score for player in self._players])

        print("The game has ended! Here are the results:")
        print(make_table(
            headers=['Player', 'Score'],
            rows=[
                [f"{p.name}{' (WINNER)' if p.score == max_score else ''}", p.score]
                for p in self._players
            ]
        ))

    def _prompt_play_again(self):
        while True:
            play_again = input("Another game? (y/N): ")
            if play_again in ['y', 'Y', 'n', 'N', '']:
                break
            else:
                print("Invalid input.")

        return play_again in ['y', 'Y']

class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py
    def test_extra_credit_task(self):
        pass

    def test_make_table(self):
        self.assertEqual(make_table(), """
--
||
--
        """.strip())

        headers=['Player', 'Score']
        rows = [['A', '3000'], ['B', '2000'], ["Joruus C'Baoth", '1000']]
        self.assertEqual(make_table(headers, rows), """
--------------------------
| Player         | Score |
|----------------|-------|
| A              | 3000  |
| B              | 2000  |
| Joruus C'Baoth | 1000  |
--------------------------
        """.strip())

        # can handle numeric values
        headers=['Player', 'Score']
        rows = [['A', 3000], ['B', 2000], ["Joruus C'Baoth", 1000]]
        self.assertEqual(make_table(headers, rows), """
--------------------------
| Player         | Score |
|----------------|-------|
| A              | 3000  |
| B              | 2000  |
| Joruus C'Baoth | 1000  |
--------------------------
        """.strip())
