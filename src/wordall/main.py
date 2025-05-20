from game_tracker import GameTracker
from rich.console import Console
import random
from pathlib import Path

# DATAFILE_PATH = Path("../data/words_5.txt")
DATAFILE_PATH = Path(__file__).parent / ".." / "data" / "words_5.txt"
console = Console(width=40)
qwerty_top = "QWERTYUIOP"
qwerty_middle = "ASDFGHJKL"
qwerty_bottom = "ZXCVBNM"

def show_results(game_stats:GameTracker):
    refresh_display()
    if not game_stats.is_solved:
        console.print("[center] Try again [/]")

    for idx in range(game_stats.max_guesses):
        guess_display = ""
        if game_stats.guesses and idx < len(game_stats.guesses):
            current_guess = game_stats.guesses[idx]
            guess_display = style_letters(current_guess, game_stats, guess_display)
        else:
            guess_display = f"[dim]______[/]"
        console.print(guess_display, justify="center")
    show_keyboard(game_stats)

    show_results_footer(game_stats)


def style_letters(current_guess, game_stats, guess_display):
    if game_stats.word == current_guess:
        guess_display = f"[bold white on green4]{current_guess}[/]"
    else:
        for gletter, wletter in zip(current_guess, game_stats.word):
            count_in_word = game_stats.word.count(gletter)
            if gletter == wletter:
                if count_in_word > 1:
                    guess_display += f"[bold white on gold3]{gletter}[/]"
                    # guess_display += f"{gletter}"
                else:
                    guess_display += f"[bold white on green4]{gletter}[/]"
                    # guess_display += f"{gletter}"
            else:
                if gletter in game_stats.word:
                    guess_display += f"[bold white on gold3]{gletter}[/]"
                else:
                    guess_display += f"[white on #666666]{gletter}[/]"
    return guess_display


def show_results_footer(game_stats):
    if game_stats.is_solved:
        console.print("[bold green]:party_popper: you got it!![/]")
        # console.print (":party_popper: you got it!!")
        console.print(game_stats.word)
    else:
        if game_stats.remaining_guesses == 0:
            console.print("[bold]:disappointed: Sorry, You are out of guesses..[/]")
            console.print(game_stats.word)


def show_keyboard(game_stats:GameTracker):
    conversion = lambda char:char if char not in game_stats.used_letters else f"[strike][bold][italics][dark_red]{char}[/][/][/][/]"
    top = ""
    middle = ""
    bottom = ""
    top = " ".join(list(map(conversion, qwerty_top)))
    middle = " ".join(list(map(conversion, qwerty_middle)))
    bottom = " ".join(list(map(conversion, qwerty_bottom)))
    console.print(top, justify="center")
    console.print(middle, justify="center")
    console.print(bottom, justify="center")

def refresh_display():
    console.clear()
    console.rule(f"[bold blue][blink]:game_die:Hello from Word-all[/blink][/bold blue]")

def main():
    word_list = [word.upper() for word in DATAFILE_PATH.read_text(encoding="utf-8").strip().split('\n')]

    chosen_word = random.choice(word_list)

    game = GameTracker(chosen_word)

    done_done:bool = False
    refresh_display()

    while not done_done:
        if game.remaining_guesses > 0:
            next_guess = console.input("Enter your next guess:-> ").upper()

            game.make_guess(next_guess)

            # game.result_matched(guess_result)
            show_results(game)
        else:
            restart = console.input(" New game? (Y/N) -> ").upper()
            if restart == 'Y':
                refresh_display()
                game.new_game(random.choice(word_list))
            else:
                done_done = True
                continue

if __name__ == "__main__":

    main()
