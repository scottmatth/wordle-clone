class GameTracker:

    word:str|None = None
    max_guesses:int = 6
    guesses = []

    def __init__(self, word):
        self.word = word

    @property
    def remaining_guesses(self):
        return 0 if (len(self.guesses) > 0 and self.word == self.guesses[-1]) else self.max_guesses - len(self.guesses)

    def make_guess(self, guess:str):
        if self.remaining_guesses < 1:
            raise UserWarning("Unable  to make any more guesses")

        self.guesses.append(guess)

    def reset(self):
        self.word = None
        self.guesses.clear()

    def new_game(self, word):
        self.reset()
        self.word = word

    @property
    def used_letters(self):
        return set([char for letters in self.guesses for char in letters ])
