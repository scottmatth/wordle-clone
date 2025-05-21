import string
from collections import defaultdict
from enum import IntEnum
class GuessStatus(IntEnum):
    NO_MATCH = 1
    WORD_MEMBER = 2
    MATCH = 3

class InvalidEntryError(ValueError):
    pass

class GameTracker:

    _word:str|None = None
    max_guesses:int = 6
    guesses:list = []
    char_tracker:dict = defaultdict()

    def __init__(self, word):
        self._word = word


    @property
    def word(self):
        return self._word if self._word else ""


    @property
    def remaining_guesses(self) -> int:
        """
        Encapsulates logic to determine if there are any remaining guesses based on eiter success or
            previous guesses
        Returns:
            integer between 0 and max_guesses which corresponds to the remaining available guesses
        """
        return 0 if (len(self.guesses) > 0 and self.is_solved) else self.max_guesses - len(self.guesses)


    def make_guess(self, guess:str):
        """
        Encapsulates the logic to update all relevant entities when a user makes a guess (i.e. adding to historical
            list of guesses for the current section)
        Args:
            guess: the guess which the user has made currently

        Returns:

        """
        if not all(alpha in string.ascii_letters for alpha in guess):
            raise InvalidEntryError("your guess can only contain values from the english alphabet  Try again.")
        if len(guess) != 5:
            raise InvalidEntryError("Your guess can be no more or less than 5 characters.  Try again.")
        if self.remaining_guesses < 1:
            raise UserWarning("Unable  to make any more guesses")

        self.guesses.append(guess)
        for char, match in zip(guess, self.word):
            if char == match:
                self.char_tracker[char] = GuessStatus.MATCH
            elif char in self.word:
                if (char not in self.char_tracker.keys() or
                        self.char_tracker[char] < GuessStatus.MATCH):
                    self.char_tracker[char] = GuessStatus.WORD_MEMBER
            else:
                self.char_tracker[char] = GuessStatus.NO_MATCH


    def _reset(self):
        """
        Wipes out the prior guesses and target word to be ready for a new game
        Returns:

        """
        self._word = None
        self.guesses.clear()
        self.char_tracker.clear()


    def new_game(self, word):
        """
        re-initializes the current instance to accept new guesses against a new word.
        Args:
            word: The word that the user is trying to guess.

        Returns:

        """
        self._reset()
        self._word = word


    @property
    def is_solved(self):
        """
        Determines if the user guesses have successfully found the word.
        Returns:
            bool if the most recent guess matches to the target word.
        """
        return self.guesses and self.word == self.guesses[-1]


    @property
    def used_letters(self) -> dict[str, GuessStatus]:
        """
        Finds the unique list of letters used in all of the guesses
        Returns:
            set of all letters used so far
        """
        return self.char_tracker
