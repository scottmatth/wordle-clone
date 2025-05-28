import pytest

from src.wordall.game_tracker import GuessStatus #type: ignore
from src.wordall.main import (_keyboard_character_format, style_guess,  #type: ignore
                              UNMATCHED_BUT_FOUND_STYLE, MACHED_STYLE,
                              NO_MATCH_STYLE)


@pytest.mark.skip
def test_show_results():
    assert False


@pytest.mark.parametrize("word, guess, styled_output",
                         [
                             ("CHEEVER", "SONNETS", f"{NO_MATCH_STYLE}S[/]{NO_MATCH_STYLE}O[/]{NO_MATCH_STYLE}N[/]"
                                                    f"{NO_MATCH_STYLE}N[/]{UNMATCHED_BUT_FOUND_STYLE}E[/]"
                                                    f"{NO_MATCH_STYLE}T[/]{NO_MATCH_STYLE}S[/]"),
                             ("SEVER", "SAVER", f"{MACHED_STYLE}S[/]{NO_MATCH_STYLE}A[/]"
                                                f"{MACHED_STYLE}V[/]{MACHED_STYLE}E[/]"
                                                f"{MACHED_STYLE}R[/]"),
                             ("SEVER", "SEVER", (f":partying_face: {MACHED_STYLE}SEVER[/] :partying_face:")),
                             ("BRAIN", "CLOSE", f"{NO_MATCH_STYLE}C[/]{NO_MATCH_STYLE}L[/]{NO_MATCH_STYLE}O[/]"
                                                f"{NO_MATCH_STYLE}S[/]{NO_MATCH_STYLE}E[/]"),
                             ("FELLAS", "FLEECE", f"{MACHED_STYLE}F[/]{UNMATCHED_BUT_FOUND_STYLE}L[/]"
                                                  f"{UNMATCHED_BUT_FOUND_STYLE}E[/]{NO_MATCH_STYLE}E[/]"
                                                  f"{NO_MATCH_STYLE}C[/]{NO_MATCH_STYLE}E[/]"),
                             ("FLAIL", "PILLS", f"{NO_MATCH_STYLE}P[/]{UNMATCHED_BUT_FOUND_STYLE}I[/]"
                                                f"{UNMATCHED_BUT_FOUND_STYLE}L[/]{UNMATCHED_BUT_FOUND_STYLE}L[/]"
                                                f"{NO_MATCH_STYLE}S[/]"),
                             ("CHIMP", "IDIOM", f"{UNMATCHED_BUT_FOUND_STYLE}I[/]{NO_MATCH_STYLE}D[/]{MACHED_STYLE}I[/]"
                                                f"{NO_MATCH_STYLE}O[/]{UNMATCHED_BUT_FOUND_STYLE}M[/]")
                         ])
def test_style_guess(word, guess, styled_output):
    assert styled_output == style_guess(guess, word)


@pytest.mark.skip
def test_show_results_footer():
    assert False


@pytest.mark.parametrize("display_content, used_list, output",
                         [
                             ("ABECWIF", {"A":GuessStatus.MATCH}, (f"{MACHED_STYLE}A[/] B E C W I F")),
                             ("ABECWIF", {"W":GuessStatus.WORD_MEMBER}, (f"A B E C {UNMATCHED_BUT_FOUND_STYLE}W[/] I F")),
                             ("ABECWIF",{"I":GuessStatus.NO_MATCH},"A B E C W [strike][bold][italics][dark_red]I[/][/][/][/] F"),
                             ("ABECWIF",{"B":GuessStatus.NO_MATCH, "C":GuessStatus.WORD_MEMBER, "F":GuessStatus.MATCH},
                              f"A [strike][bold][italics][dark_red]B[/][/][/][/] E {UNMATCHED_BUT_FOUND_STYLE}C[/] W I {MACHED_STYLE}F[/]"),
                         ]
                         )
def test__keyboard_character_format(display_content, used_list, output):
    assert output == _keyboard_character_format(display_content, used_list)


@pytest.mark.skip
def test_show_keyboard():
    assert False


@pytest.mark.skip
def test_refresh_display():
    assert False
