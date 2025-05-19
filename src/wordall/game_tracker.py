from collections import defaultdict

class GameTracker:

    word:str|None = None
    max_guesses:int = 6
    guesses = []

    def __init__(self, word):
        self.word = word

    @property
    def remaining_guesses(self):
        return 0 if (len(self.guesses) > 0 and self.word == self.guesses[-1]) else self.max_guesses - len(self.guesses)

    def make_guess(self, guess:str) -> dict[str, list]:
        capture = defaultdict(list)
        if self.remaining_guesses < 1:
            raise UserWarning("Unable  to make any more guesses")

        if guess == self.word:
            capture = {char:["GOTIT"] for char in guess}
        else:
            for guess_char, real_char in zip(guess, self.word):
                if guess not in self.word:
                    capture[guess_char].append("NOPE")
                elif guess_char == real_char:
                    capture[guess_char].append("GOTIT")
        self.guesses.append(guess)
        return capture

    def reset(self):
        self.word = None
        self.guesses.clear()

    def new_game(self, word):
        self.reset()
        self.word = word

    @staticmethod
    def result_matched(guess_result:dict[str, list]):
        return all(a == ["GOTIT"] for a in guess_result.values())



