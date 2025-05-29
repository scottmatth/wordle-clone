import pytest

from src.wordall.game_tracker import GameTracker, InvalidEntryError #type: ignore


@pytest.fixture
def basic_game():
    return GameTracker("SEVER")


@pytest.mark.parametrize("word,size",
                         [
                             ("SEVER", None),
                             ("SEVER", 5),
                             ("CHERUB", None),
                             ("CHERUB", 6),
                         ])
def test_construct_tracker(word,size):
    if size:
        game = GameTracker(word, size)
    else:
        game = GameTracker(word)

    assert game.word == word
    assert game.word_size == size if size else 5


def test_word(basic_game:GameTracker):
    assert basic_game.word == "SEVER"
    assert basic_game.word != "sever"


@pytest.mark.parametrize("word, size, guesses, assertion",
                         [
                             ("SEVER", 5, [], 6),
                             ("SEVER", 5, ["EVENT"], 5),
                             ("SEVER", 5, ["EVENT","SAVER"], 4),
                             ("SEVER", 5, ["EVENT","SAVER", "SEVER"], 0),
                             ("CHERUB", 6, [], 6),
                             ("CHERUB", 6, ["CHASED"], 5),
                             ("CHERUB", 6, ["CHASED", "CHOSEN"], 4),
                             ("CHERUB", 6, ["CHASED", "CHOSEN", "CHERUB"], 0),
                             ("CHERUB", 6, ["CHERUB"], 0),
                         ])
def test_remaining_guesses(word, size, guesses:list,
                           assertion:int):
    basic_game = GameTracker(word, size)
    for guess in guesses:
        basic_game.make_guess(guess)
    assert basic_game.remaining_guesses == assertion


@pytest.mark.parametrize("word, size, scenario, error",
                         [
                             pytest.param("SEVER", 5,"STAKES", "Your guess can be no more or less than 5 characters.  Try again.", id="Guess too long"),
                             pytest.param("SEVER", 5,"SO", "Your guess can be no more or less than 5 characters.  Try again.", id="Guess too short"),
                             pytest.param("SEVER", 5,"SO_SO", "your guess can only contain values from the english alphabet  Try again.", id="Guess too has invalid characters"),
                             pytest.param("CHERUB", 6,"STINKES", "Your guess can be no more or less than 6 characters.  Try again.", id="Guess too long 6 characters"),
                             pytest.param("CHERUB", 6,"SO", "Your guess can be no more or less than 6 characters.  Try again.", id="Guess too short 6 characters"),
                             pytest.param("CHERUB", 6,"SO__SO", "your guess can only contain values from the english alphabet  Try again.", id="Guess too has invalid characters 6 characters"),
                         ])
def test_make_failing_guess(word, size, scenario, error):
    basic_game = GameTracker(word, size)
    try:
        basic_game.make_guess(scenario)
        assert False
    except InvalidEntryError as test_e:
        assert str(test_e) == error

    # Now make the correct guess to halt guesses
    basic_game.make_guess(word)
    # Now try to make ONE MORE guess
    try:
        basic_game.make_guess("AERIE"+("" if size == 5 else "S"))
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
    assert not basic_game.is_solved
    for guess in scenarios:
        basic_game.make_guess(guess)
    assert basic_game.remaining_guesses == guesses_left
    assert basic_game.is_solved == is_it_solved

@pytest.mark.parametrize("scenarios, used_letter_list",
                         [
                             pytest.param([], [], id="No Guess."),
                             pytest.param(["SEVER"], ['S', 'E', 'R', 'V'], id="correct guess."),
                             pytest.param(["AERIE"], ['A', 'R', 'E', 'I'], id="invalid guess."),
                             pytest.param(["AERIE","EVENT","SAVER", "SEVER"], ['A', 'R', 'E', 'I', 'V', 'N', 'T', 'S'], id="Correct guess after bad."),
                             pytest.param(["AERIE","EVENT","SAVER", "SLIDE", "ABIDE", "CHIDE"], ['A', 'R', 'E', 'I', 'V', 'N', 'T', 'S', 'B', 'D', 'I', 'C', 'H'], id="Full invalid guesses."),
                         ])
def test_used_letters(basic_game:GameTracker,scenarios, used_letter_list):
    assert not basic_game.used_letters.keys()
    for guess in scenarios:
        basic_game.make_guess(guess)

    assert len(basic_game.used_letters) == len(used_letter_list)
    for letter in used_letter_list:
        assert letter in basic_game.used_letters.keys()
