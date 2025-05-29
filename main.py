import random
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

from src.wordall.game_tracker import GameTracker, InvalidEntryError  # type: ignore
from src.wordall.utilities import show_results, refresh_display  # type: ignore

FIVE_WORD_DATAFILE_PATH = Path(__file__).parent / "src" / "data" / "words_5.txt"
SIX_WORD_DATAFILE_PATH = Path(__file__).parent / "src" / "data" / "words_6.txt"

console = Console(width=40)

def main():

    refresh_display(console)

    word_size = Prompt.ask("5 word or 6 word game (Click Enter for the default)? -> ", default=5)

    word_source = FIVE_WORD_DATAFILE_PATH if int(word_size) == 5 else SIX_WORD_DATAFILE_PATH
    word_list = [word.upper() for word in word_source.read_text(encoding="utf-8").strip().split('\n')]

    chosen_word = random.choice(word_list)

    game = GameTracker(chosen_word, int(word_size))

    finished:bool = False  # type: ignore

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
