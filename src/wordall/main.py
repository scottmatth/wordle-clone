from rich import print
from wordall.src.wordall import DATAFILE_PATH
from game_tracker import GameTracker
import random


def show_results(game_stats:GameTracker, results:dict = None):
    success = game_stats.word == game_stats.guesses[-1]
    if success:
        print ("you got it!!")
    print(game_stats.word)
    print(game_stats.guesses)


def main():
    print("Hello from wordall!")
    word_list = [word.upper() for word in DATAFILE_PATH.read_text(encoding="utf-8").strip().split('\n')]

    chosen_word = random.choice(word_list)

    game = GameTracker(chosen_word)

    done_done:bool = False

    while not done_done:
        if game.remaining_guesses > 0:
            next_guess = input("Enter your next guess:-> ")

            guess_result = game.make_guess(next_guess.upper())

            game.result_matched(guess_result)
            show_results(game, guess_result)
        else:
            restart = input("You are out of guesses. New game? (Y/N) -> ")
            if restart.upper() == 'Y':
                game.new_game(random.choice(word_list))
            else:
                done_done = True
                continue

if __name__ == "__main__":

    main()
