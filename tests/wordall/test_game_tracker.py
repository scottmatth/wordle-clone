import pytest

from src.wordall.game_tracker import GameTracker
from src.wordall.game_tracker import InvalidEntryError


@pytest.fixture
def basic_game():
    return GameTracker("SEVER")


def test_word(basic_game:GameTracker):
    assert basic_game.word == "SEVER"
    assert basic_game.word != "sever"


@pytest.mark.parametrize("guesses, assertion",
                         [
                             ([], 6),
                             (["EVENT"], 5),
                             (["EVENT","SAVER"], 4),
                             (["EVENT","SAVER", "SEVER"], 0),
                         ])
def test_remaining_guesses(basic_game:GameTracker, guesses:list,
                           assertion:int):
    for guess in guesses:
        basic_game.make_guess(guess)
    assert basic_game.remaining_guesses == assertion


@pytest.mark.parametrize("scenario, error",
                         [
                             pytest.param("STAKES", "Your guess can be no more or less than 5 characters.  Try again.", id="Guess too long"),
                             pytest.param("SO", "Your guess can be no more or less than 5 characters.  Try again.", id="Guess too short"),
                             pytest.param("SO_SO", "your guess can only contain values from the english alphabet  Try again.", id="Guess too has invalid characters"),
                         ])
def test_make_failing_guess(basic_game:GameTracker, scenario, error):
    try:
        basic_game.make_guess(scenario)
        assert False
    except InvalidEntryError as test_e:
        assert str(test_e) == error

    # Now make the correct guess to halt guesses
    basic_game.make_guess("SEVER")
    # Now try to make ONE MORE guess
    try:
        basic_game.make_guess("AERIE")
        assert False
    except UserWarning as uw:
        assert str(uw) == "Unable to make any more guesses"


def test__reset(basic_game:GameTracker):
    basic_game.make_guess("AERIE")
    assert basic_game.word
    assert basic_game.remaining_guesses < 6
    assert basic_game.guesses

    basic_game._reset()
    assert not basic_game.word
    assert basic_game.remaining_guesses == 6
    assert not basic_game.guesses


def test_new_game(basic_game:GameTracker):
    basic_game.make_guess("AERIE")
    assert basic_game.word
    assert basic_game.remaining_guesses < 6
    assert basic_game.guesses

    basic_game.new_game("SAVER")
    assert basic_game.word == "SAVER"
    assert basic_game.remaining_guesses == 6
    assert not basic_game.guesses


@pytest.mark.parametrize("scenarios, guesses_left, is_it_solved",
                         [
                             pytest.param([], 6, False, id="No Guess.  Not solved"),
                             pytest.param(["SEVER"], 0, True, id="correct guess.  Solved"),
                             pytest.param(["AERIE"], 5, False, id="invalid guess.  Not solved"),
                             pytest.param(["AERIE","EVENT","SAVER", "SEVER"], 0, True, id="Correct guess after bad.  Solved"),
                             pytest.param(["AERIE","EVENT","SAVER", "SLIDE", "ABIDE", "CHIDE"], 0, False, id="Full invalid guesses.  Not Solved"),
                         ])
def test_is_solved(basic_game:GameTracker, scenarios,
                   guesses_left, is_it_solved):
    assert basic_game.is_solved == False
    for guess in scenarios:
        basic_game.make_guess(guess)
    assert basic_game.remaining_guesses == guesses_left
    assert basic_game.is_solved == is_it_solved

@pytest.mark.parametrize("scenarios, used_letter_list",
                         [
                             pytest.param([], [], id="No Guess."),
                             pytest.param(["SEVER"], ['S', 'E', 'R'], id="correct guess."),
                             pytest.param(["AERIE"], ['A', 'R', 'E', 'I'], id="invalid guess."),
                             pytest.param(["AERIE","EVENT","SAVER", "SEVER"], ['A', 'R', 'E', 'I', 'V', 'N', 'T', 'S'], id="Correct guess after bad."),
                             pytest.param(["AERIE","EVENT","SAVER", "SLIDE", "ABIDE", "CHIDE"], ['A', 'R', 'E', 'I', 'V', 'N', 'T', 'S', 'B', 'D', 'I', 'C', 'H'], id="Full invalid guesses."),
                         ])
def test_used_letters(basic_game:GameTracker,scenarios, used_letter_list):
    assert not basic_game.used_letters.keys()
    for guess in scenarios:
        basic_game.make_guess(guess)

    for letter in used_letter_list:
        assert letter in basic_game.used_letters.keys()
