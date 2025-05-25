import random
from collections import defaultdict
from pathlib import Path

from rich.console import Console

from game_tracker import GameTracker, InvalidEntryError, GuessStatus  # type: ignore

DATAFILE_PATH = Path(__file__).parent / ".." / "data" / "words_5.txt"
QWERTY_TOP = "QWERTYUIOP"
QWERTY_MIDDLE = "ASDFGHJKL"
QWERTY_BOTTOM = "ZXCVBNM"

console = Console(width=40)


def show_results(game_stats:GameTracker):
    """
    Encapsulates the logic to print the historic guesses and their status,
    the keyboard characters with indication of usage, and whether or not a
    match happened occurred.
    Args:
        game_stats: Representation of the details of the current game.  Gives access
            to the word, historical guesses, and other methods to help with game evaluation
    """
    refresh_display()
    if not game_stats.is_solved:
        console.print("[center] Try again [/]")

    for idx in range(game_stats.max_guesses):
        if game_stats.guesses and idx < len(game_stats.guesses):
            current_guess = game_stats.guesses[idx]
            guess_display = style_guess(current_guess, game_stats.word)
        else:
            guess_display = f"[dim]______[/]"
        console.print(guess_display, justify="center")
    show_keyboard(game_stats.char_tracker)

    show_results_footer(game_stats)


def style_guess(current_guess, target_word:str):
    """
    Used for each line of the display for historical guesses.  Will apply the appropriate
    rich styling to indicate the status of the letters in the guess
    Args:
        current_guess:
            Latest guess made by the user
        target_word:
            The word to which all guesses in this game session attempt to match

    Returns:
        The guess with styling brackets around it to display with context to the target word
    """
    display=""
    if target_word == current_guess:
        display = f":partying_face: [bold white on green4]{current_guess}[/] :partying_face:"
    else:
        track:dict = defaultdict()
        #
        for gletter, wletter in zip(current_guess, target_word):
            if gletter == wletter:
                track[gletter] = GuessStatus.MATCH
                display += f"[bold white on green4]{gletter}[/]"
            else:
                if gletter in target_word:
                    display += f"[bold white on gold3]{gletter}[/]"
                else:
                    track[gletter] = GuessStatus.NO_MATCH
                    display += f"[white on #666666]{gletter}[/]"
    return display


def show_results_footer(game_stats):
    """
    Encapsulates the logic intended to be displayed at the end of a game.  Lets the
    player know if they solved it or they are out of any more guesses.
    Args:
        game_stats:  stores the data for the current game session such as the target word, guesses, etc.
    """
    if game_stats.is_solved:
        console.print("[bold green]:party_popper: you got it!![/]")
        # console.print (":party_popper: you got it!!")
        console.print(game_stats.word)
    else:
        if game_stats.remaining_guesses == 0:
            console.print("[bold]:disappointed: Sorry, You are out of guesses..[/]")
            console.print(game_stats.word)


def _keyboard_character_format(keyboard_row:str,
                               used_letter_map:dict[str, GuessStatus]) -> str:
    """
    Encapsulates the logic to format each row of the keyboard section with context to character used

    Args:
        keyboard_row: list of keyboard letters to which a format is intended to be applied
        used_letter_map: Map of the letters which have been used and the context of their status relative
            to the target word

    Returns:
        formated string containing all row members
    """
    formatted_output = []
    for char in keyboard_row:
        formatted_char = char
        if char in used_letter_map.keys():
            match used_letter_map[char]:
                case GuessStatus.NO_MATCH:
                    formatted_char = f"[strike][bold][italics][dark_red]{char}[/][/][/][/]"
                case GuessStatus.WORD_MEMBER:
                    formatted_char = f"[bold white on gold3]{char}[/]"
                case GuessStatus.MATCH:
                    formatted_char = f"[bold white on green4]{char}[/]"
        formatted_output.append(formatted_char)
    return " ".join(formatted_output)


def show_keyboard(used_letter_map:dict[str, GuessStatus]):
    """
    Encapsulates the logic to display the used/unused keyboard letters to the user
    Args:
        used_letter_map: map of letters used and their context to prior guesses

    """
    console.print(_keyboard_character_format(QWERTY_TOP, used_letter_map), justify="center")
    console.print(_keyboard_character_format(QWERTY_MIDDLE, used_letter_map), justify="center")
    console.print(_keyboard_character_format(QWERTY_BOTTOM, used_letter_map), justify="center")


def refresh_display():
    """
    Restarts the display anew to show updates to the game (e.g. new results, new input prompts, etc.)
    """
    console.clear()
    console.rule(f"[bold blue][blink] :game_die: Hello from Word-all[/blink][/bold blue]")


def main():
    word_list = [word.upper() for word in DATAFILE_PATH.read_text(encoding="utf-8").strip().split('\n')]

    chosen_word = random.choice(word_list)

    game = GameTracker(chosen_word)

    done_done:bool = False  # type: ignore
    refresh_display()

    while not done_done:
        if game.remaining_guesses > 0:
            next_guess = console.input("Enter your next guess:-> ").upper()

            try:
                game.make_guess(next_guess)
                show_results(game)
            except InvalidEntryError as iee:
                console.print(iee)
        else:
            restart = console.input(" New game? (Y/N) -> ").upper()
            if restart == 'Y':
                refresh_display()
                game.new_game(random.choice(word_list))
            else:
                done_done = True

if __name__ == "__main__":

    main()
