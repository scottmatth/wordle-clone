"""Houses the class definition and logic for tracking and supporting a running Wordall game"""

import string
from collections import defaultdict
from enum import IntEnum
from typing import Any

from pydantic import BaseModel


class GuessStatus(IntEnum):
    """
    Enum to support matching guesses to selected words
    """

    NO_MATCH = 1
    WORD_MEMBER = 2
    MATCH = 3


class InvalidEntryError(ValueError):
    """
    Representation of an error condition when the input which the user has made is invalid with
    respect to the rules of the game.
    """


class GameTracker(BaseModel):
    """
    Definition of the session state for the running game.  Will represent all necessary information
    to allow a user to run the game
    """

    max_guesses: int = 6
    guesses: list = []
    char_tracker: dict = defaultdict()

    def __init__(self, word, word_length=5, **data: Any):
        """
        Constructor for the Wordle clone game

        Args:
            word: Word against which the game will run against
            **data:
        """
        super().__init__(**data)
        self._word = word
        self._word_length = word_length

    @property
    def word(self):
        """
        Accessor for the defined word to be used for the game
        Returns:
            Value of the word with which the given game session has been initialized
        """
        return self._word if self._word else ""

    @property
    def word_size(self):
        """
        Accessor for the configured size of the target word for the game
        Returns:
            Int value of size of the word with which the given game session has been initialized
        """
        return self._word_length

    @property
    def remaining_guesses(self) -> int:
        """
        Encapsulates logic to determine if there are any remaining guesses based on eiter success or
            previous guesses
        Returns:
            integer between 0 and max_guesses which corresponds to the remaining available guesses
        """
        return (
            0
            if (len(self.guesses) > 0 and self.is_solved)
            else self.max_guesses - len(self.guesses)
        )

    def make_guess(self, guess: str):
        """
        Encapsulates the logic to update all relevant entities when a user makes a guess (i.e.
            adding to historical list of guesses for the current section)
        Args:
            guess: the guess which the user has made currently
        """
        if not all(alpha in string.ascii_letters for alpha in guess):
            raise InvalidEntryError(
                "your guess can only contain values from the english alphabet. "
                "Try again."
            )
        if len(guess) != self.word_size:
            raise InvalidEntryError(
                f"Your guess can be no more or less than {self.word_size} "
                f"characters. Try again."
            )
        if self.remaining_guesses < 1:
            raise UserWarning("Unable to make any more guesses")

        self.guesses.append(guess)
        for char, match in zip(guess, self.word):
            if char == match:
                self.char_tracker[char] = GuessStatus.MATCH
            elif char in self.word:
                if (
                    char not in self.char_tracker.keys()
                    or self.char_tracker[char] < GuessStatus.MATCH
                ):
                    self.char_tracker[char] = GuessStatus.WORD_MEMBER
            else:
                self.char_tracker[char] = GuessStatus.NO_MATCH

    def reset(self):
        """
        Wipes out the prior guesses and target word to be ready for a new game
        Returns:

        """
        self._word = None
        self.guesses.clear()
        self.char_tracker.clear()

    def new_game(self, word, word_length=None):
        """
        re-initializes the current instance to accept new guesses against a new word.
        Args:
            word_length:
            word: The word that the user is trying to guess.

        Returns:

        """
        self.reset()
        self._word = word
        if word_length:
            self._word_length = word_length

    @property
    def is_solved(self) -> bool:
        """
        Determines if the user guesses have successfully found the word.
        Returns:
            bool if the most recent guess matches to the target word.
        """
        return not (
            not self.guesses or not (self.word == self.guesses[-1])
        )  # pylint: disable=C0325

    @property
    def used_letters(self) -> dict[str, GuessStatus]:
        """
        Finds the unique list of letters used in all of the guesses
        Returns:
            set of all letters used so far
        """
        return self.char_tracker
