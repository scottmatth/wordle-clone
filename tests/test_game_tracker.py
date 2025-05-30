"""
Stores unit tests to assist in testing the Wordall functionality ensuring that nothing has been
missed
"""

import pytest

from src.wordall.game_tracker import GameTracker, InvalidEntryError  # type: ignore


@pytest.fixture(name="game_fixture")
def basic_game():  # pylint: disable=C0116
    """
    Basic fixture for testing Wordall game scenarios
    Returns:
    A basic instance of a game session to use in some of the unit tests below
    """
    return GameTracker("SEVER")


@pytest.mark.parametrize(
    "word,size",
    [
        ("SAVER", None),
        ("PAVER", 5),
        ("CHERUB", None),
        ("CHERRY", 6),
    ],
)
def test_construct_tracker(word, size):  # pylint: disable=C0116
    if size:
        game = GameTracker(word, size)
    else:
        game = GameTracker(word)

    assert game.word == word
    assert game.word_size == size if size else 5


def test_word(game_fixture):  # pylint: disable=C0116
    assert game_fixture.word == "SEVER"
    assert game_fixture.word != "sever"


@pytest.mark.parametrize(
    "word, size, guesses, assertion",
    [
        ("SEVER", 5, [], 6),
        ("SEVER", 5, ["EVENT"], 5),
        ("SEVER", 5, ["EVENT", "SAVER"], 4),
        ("SEVER", 5, ["EVENT", "SAVER", "SEVER"], 0),
        ("CHERUB", 6, [], 6),
        ("CHERUB", 6, ["CHASED"], 5),
        ("CHERUB", 6, ["CHASED", "CHOSEN"], 4),
        ("CHERUB", 6, ["CHASED", "CHOSEN", "CHERUB"], 0),
        ("CHERUB", 6, ["CHERUB"], 0),
    ],
)
def test_remaining_guesses(  # pylint: disable=C0116
    word, size, guesses: list, assertion: int
):
    game_scope = GameTracker(word, size)
    for guess in guesses:
        game_scope.make_guess(guess)
    assert game_scope.remaining_guesses == assertion


@pytest.mark.parametrize(
    "word, size, scenario, error",
    [
        pytest.param(
            "SEVER",
            5,
            "STAKES",
            "Your guess can be no more or less than 5 characters. Try again.",
            id="Guess too long",
        ),
        pytest.param(
            "SEVER",
            5,
            "SO",
            "Your guess can be no more or less than 5 characters. Try again.",
            id="Guess too short",
        ),
        pytest.param(
            "SEVER",
            5,
            "SO_SO",
            "your guess can only contain values from the english alphabet. Try again.",
            id="Guess too has invalid characters",
        ),
        pytest.param(
            "CHERUB",
            6,
            "STINKES",
            "Your guess can be no more or less than 6 characters. Try again.",
            id="Guess too long 6 characters",
        ),
        pytest.param(
            "CHERUB",
            6,
            "SO",
            "Your guess can be no more or less than 6 characters. Try again.",
            id="Guess too short 6 characters",
        ),
        pytest.param(
            "CHERUB",
            6,
            "SO__SO",
            "your guess can only contain values from the english "
            "alphabet. Try again.",
            id="Guess too has invalid characters 6 characters",
        ),
    ],
)
def test_make_failing_guess(word, size, scenario, error):  # pylint: disable=C0116
    game_scope = GameTracker(word, size)
    try:
        game_scope.make_guess(scenario)
        assert False
    except InvalidEntryError as test_e:
        assert str(test_e) == error

    # Now make the correct guess to halt guesses
    game_scope.make_guess(word)
    # Now try to make ONE MORE guess
    try:
        game_scope.make_guess("AERIE" + ("" if size == 5 else "S"))
        assert False
    except UserWarning as uw:
        assert str(uw) == "Unable to make any more guesses"


def test__reset(game_fixture: GameTracker):  # pylint: disable=C0116
    game_fixture.make_guess("AERIE")
    assert game_fixture.word
    assert game_fixture.remaining_guesses < 6
    assert game_fixture.guesses

    game_fixture.reset()
    assert not game_fixture.word
    assert game_fixture.remaining_guesses == 6
    assert not game_fixture.guesses


def test_new_game(game_fixture: GameTracker):  # pylint: disable=C0116
    game_fixture.make_guess("AERIE")
    assert game_fixture.word
    assert game_fixture.remaining_guesses < 6
    assert game_fixture.guesses

    game_fixture.new_game("SAVERS", 6)
    assert game_fixture.word == "SAVERS"
    assert game_fixture.remaining_guesses == 6
    assert game_fixture.word_size == 6
    assert not game_fixture.guesses


@pytest.mark.parametrize(
    "scenarios, guesses_left, is_it_solved",
    [
        pytest.param([], 6, False, id="No Guess.  Not solved"),
        pytest.param(["SEVER"], 0, True, id="correct guess. Solved"),
        pytest.param(["AERIE"], 5, False, id="invalid guess. Not solved"),
        pytest.param(
            ["AERIE", "EVENT", "SAVER", "SEVER"],
            0,
            True,
            id="Correct guess after bad.  Solved",
        ),
        pytest.param(
            ["AERIE", "EVENT", "SAVER", "SLIDE", "ABIDE", "CHIDE"],
            0,
            False,
            id="Full invalid guesses.  Not Solved",
        ),
    ],
)
def test_is_solved(  # pylint: disable=C0116
    game_fixture: GameTracker,
    scenarios,
    guesses_left,
    is_it_solved,
):
    assert not game_fixture.is_solved
    for guess in scenarios:
        game_fixture.make_guess(guess)
    assert game_fixture.remaining_guesses == guesses_left
    assert game_fixture.is_solved == is_it_solved


@pytest.mark.parametrize(
    "scenarios, used_letter_list",
    [
        pytest.param([], [], id="No Guess."),
        pytest.param(["SEVER"], ["S", "E", "R", "V"], id="correct guess."),
        pytest.param(["AERIE"], ["A", "R", "E", "I"], id="invalid guess."),
        pytest.param(
            ["AERIE", "EVENT", "SAVER", "SEVER"],
            ["A", "R", "E", "I", "V", "N", "T", "S"],
            id="Correct guess after bad.",
        ),
        pytest.param(
            ["AERIE", "EVENT", "SAVER", "SLIDE", "ABIDE", "CHIDE"],
            ["A", "R", "E", "I", "V", "N", "T", "S", "B", "D", "I", "C", "H"],
            id="Full invalid guesses.",
        ),
    ],
)
def test_used_letters(  # pylint: disable=C0116
    game_fixture: GameTracker, scenarios, used_letter_list
):
    assert not game_fixture.used_letters.keys()
    for guess in scenarios:
        game_fixture.make_guess(guess)

    assert len(game_fixture.used_letters) == len(used_letter_list)
    for letter in used_letter_list:
        assert letter in game_fixture.used_letters.keys()
