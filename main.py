import random
from pathlib import Path

from rich.console import Console

from src.wordall.game_tracker import GameTracker, InvalidEntryError, GuessStatus  # type: ignore
from src.wordall.utilities import show_results, refresh_display  # type: ignore

DATAFILE_PATH = Path(__file__).parent / "src" / "data" / "words_5.txt"

console = Console(width=40)

def main():
    word_list = [word.upper() for word in DATAFILE_PATH.read_text(encoding="utf-8").strip().split('\n')]

    chosen_word = random.choice(word_list)

    game = GameTracker(chosen_word)

    finished:bool = False  # type: ignore
    refresh_display(console)

    while not finished:
        if game.remaining_guesses > 0:
            next_guess = console.input("Enter your next guess:-> ").upper()

            try:
                game.make_guess(next_guess)
                show_results(game, console)
            except InvalidEntryError as iee:
                console.print(iee)
        else:
            restart = console.input(" New game? (Y/N) -> ").upper()
            if restart == 'Y':
                refresh_display(console)
                game.new_game(random.choice(word_list))
            else:
                finished = True

if __name__ == "__main__":

    main()
