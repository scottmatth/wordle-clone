import pytest

from src.wordall.game_tracker import GuessStatus #type: ignore
from src.wordall.utilities import (keyboard_character_format, style_guess,  #type: ignore
                                   UNMATCHED_BUT_FOUND_STYLE, MATCHED_STYLE,
                                   NO_MATCH_STYLE)


@pytest.mark.skip
def test_show_results():
    assert False


@pytest.mark.parametrize("word, guess, styled_output",
                         [
                             ("CHEEVER", "SONNETS", f"{NO_MATCH_STYLE}S[/]{NO_MATCH_STYLE}O[/]{NO_MATCH_STYLE}N[/]"
                                                    f"{NO_MATCH_STYLE}N[/]{UNMATCHED_BUT_FOUND_STYLE}E[/]"
                                                    f"{NO_MATCH_STYLE}T[/]{NO_MATCH_STYLE}S[/]"),
                             ("SEVER", "SAVER", f"{MATCHED_STYLE}S[/]{NO_MATCH_STYLE}A[/]"
                                                f"{MATCHED_STYLE}V[/]{MATCHED_STYLE}E[/]"
                                                f"{MATCHED_STYLE}R[/]"),
                             ("SEVER", "SEVER", f":partying_face: {MATCHED_STYLE}SEVER[/] :partying_face:"),
                             ("BRAIN", "CLOSE", f"{NO_MATCH_STYLE}C[/]{NO_MATCH_STYLE}L[/]{NO_MATCH_STYLE}O[/]"
                                                f"{NO_MATCH_STYLE}S[/]{NO_MATCH_STYLE}E[/]"),
                             ("FELLAS", "FLEECE", f"{MATCHED_STYLE}F[/]{UNMATCHED_BUT_FOUND_STYLE}L[/]"
                                                  f"{UNMATCHED_BUT_FOUND_STYLE}E[/]{NO_MATCH_STYLE}E[/]"
                                                  f"{NO_MATCH_STYLE}C[/]{NO_MATCH_STYLE}E[/]"),
                             ("FLAIL", "PILLS", f"{NO_MATCH_STYLE}P[/]{UNMATCHED_BUT_FOUND_STYLE}I[/]"
                                                f"{UNMATCHED_BUT_FOUND_STYLE}L[/]{UNMATCHED_BUT_FOUND_STYLE}L[/]"
                                                f"{NO_MATCH_STYLE}S[/]"),
                             ("CHIMP", "IDIOM", f"{NO_MATCH_STYLE}I[/]{NO_MATCH_STYLE}D[/]{MATCHED_STYLE}I[/]"
                                                f"{NO_MATCH_STYLE}O[/]{UNMATCHED_BUT_FOUND_STYLE}M[/]"),
                             ("IMPRESSED", "STRESSEDA", f"{UNMATCHED_BUT_FOUND_STYLE}S[/]{NO_MATCH_STYLE}T[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}R[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}E[/]"
                                                        f"{NO_MATCH_STYLE}S[/]{MATCHED_STYLE}S[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}E[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}D[/]"
                                                        f"{NO_MATCH_STYLE}A[/]"),
                             ("IMPRSSEDE", "STRESSEDA", f"{NO_MATCH_STYLE}S[/]{NO_MATCH_STYLE}T[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}R[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}E[/]"
                                                        f"{MATCHED_STYLE}S[/]{MATCHED_STYLE}S[/]"
                                                        f"{MATCHED_STYLE}E[/]"
                                                        f"{MATCHED_STYLE}D[/]"
                                                        f"{NO_MATCH_STYLE}A[/]"),
                             ( "STRESSEDA", "IMPRSSEDE", f"{NO_MATCH_STYLE}I[/]{NO_MATCH_STYLE}M[/]"
                                                        f"{NO_MATCH_STYLE}P[/]"
                                                        f"{UNMATCHED_BUT_FOUND_STYLE}R[/]"
                                                        f"{MATCHED_STYLE}S[/]{MATCHED_STYLE}S[/]"
                                                        f"{MATCHED_STYLE}E[/]"
                                                        f"{MATCHED_STYLE}D[/]"
                                                        f"{NO_MATCH_STYLE}E[/]"),
                             ("STINT", "IDIOM", f"{NO_MATCH_STYLE}I[/]{NO_MATCH_STYLE}D[/]{MATCHED_STYLE}I[/]"
                                                f"{NO_MATCH_STYLE}O[/]{NO_MATCH_STYLE}M[/]"),
                             ("SPENT", "EASED",f"{UNMATCHED_BUT_FOUND_STYLE}E[/]{NO_MATCH_STYLE}A[/]"
                                               f"{UNMATCHED_BUT_FOUND_STYLE}S[/]{NO_MATCH_STYLE}E[/]{NO_MATCH_STYLE}D[/]")
                         ])
def test_style_guess(word, guess, styled_output):
    assert styled_output == style_guess(guess, word)


@pytest.mark.skip
def test_show_results_footer():
    assert False


@pytest.mark.parametrize("display_content, used_list, output",
                         [
                             ("ABECWIF", {"A":GuessStatus.MATCH}, f"{MATCHED_STYLE}A[/] B E C W I F"),
                             ("ABECWIF", {"W":GuessStatus.WORD_MEMBER}, f"A B E C {UNMATCHED_BUT_FOUND_STYLE}W[/] I F"),
                             ("ABECWIF",{"I":GuessStatus.NO_MATCH},"A B E C W [strike][bold][italics][dark_red]I[/][/][/][/] F"),
                             ("ABECWIF",{"B":GuessStatus.NO_MATCH, "C":GuessStatus.WORD_MEMBER, "F":GuessStatus.MATCH},
                              f"A [strike][bold][italics][dark_red]B[/][/][/][/] E {UNMATCHED_BUT_FOUND_STYLE}C[/] W I {MATCHED_STYLE}F[/]"),
                         ]
                         )
def test__keyboard_character_format(display_content, used_list, output):
    assert output == keyboard_character_format(display_content, used_list)


@pytest.mark.skip
def test_show_keyboard():
    assert False


@pytest.mark.skip
def test_refresh_display():
    assert False
