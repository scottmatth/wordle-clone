from .game_tracker import GameTracker, GuessStatus #type: ignore

QWERTY_TOP = "QWERTYUIOP"
QWERTY_MIDDLE = "ASDFGHJKL"
QWERTY_BOTTOM = "ZXCVBNM"
UNMATCHED_BUT_FOUND_STYLE = "[bold white on gold3]"
MATCHED_STYLE = "[bold white on green4]"
NO_MATCH_STYLE = "[white on #666666]"


def show_results(game_stats:GameTracker, console_in):
    """
    Encapsulates the logic to print the historic guesses and their status,
    the keyboard characters with indication of usage, and whether or not a
    match happened occurred.
    Args:
        console_in:  Reference to the Rich Console with which the display shall be printed
        game_stats: Representation of the details of the current game.  Gives access
            to the word, historical guesses, and other methods to help with game evaluation
    """
    refresh_display(console_in)
    if not game_stats.is_solved:
        console_in.print("[center] Try again [/]")

    for idx in range(game_stats.max_guesses):
        if game_stats.guesses and idx < len(game_stats.guesses):
            current_guess = game_stats.guesses[idx]
            guess_display = style_guess(current_guess, game_stats.word)
        else:
            guess_display = f"[dim]{'_'*game_stats.word_size}[/]"
        console_in.print(guess_display, justify="center")
    show_keyboard(game_stats.char_tracker, console_in)

    show_results_footer(game_stats, console_in)


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
        display = f":partying_face: {MATCHED_STYLE}{current_guess}[/] :partying_face:"
    else:
        # Assist in letter match hints by counting how many times each letter appears in the target word
        track_highlights:dict = {letter:target_word.count(letter) for letter in current_guess}

        for gletter, wletter in zip(current_guess, target_word):
            # Deduct the count by each matched letter so that it truly just matches highlights
            if gletter == wletter:
                track_highlights[gletter] -= 1

        # Compare the guess to the chosen word letter by letter and apply styling
        for gletter, wletter in zip(current_guess, target_word):
            if gletter == wletter:
                # Display green highlight if letters match
                display += f"{MATCHED_STYLE}{gletter}[/]"
            elif gletter in target_word:
                if gletter in target_word and track_highlights[gletter] >= 1:
                    # Display yellow highlight if doesn't match ANd the letter exists AND we have enough
                    # unmatched representations left
                    display += f"{UNMATCHED_BUT_FOUND_STYLE}{gletter}[/]"
                else:
                    # If no other highlights left, show that it does not match
                    display += f"{NO_MATCH_STYLE}{gletter}[/]"
            else:
                # All other mathces fail, Show that it does not match
                display += f"{NO_MATCH_STYLE}{gletter}[/]"
            if track_highlights[gletter] > 0:
                # Decrement the number of tracked Highlights to mark off when they should not be used anymore
                track_highlights[gletter] -= 1
    return display


def show_results_footer(game_stats, console_in):
    """
    Encapsulates the logic intended to be displayed at the end of a game.  Lets the
    player know if they solved it or they are out of any more guesses.
    Args:
        console_in: Reference to the Rich Console with which the display shall be printed
        game_stats:  stores the data for the current game session such as the target word, guesses, etc.
    """
    if game_stats.is_solved:
        console_in.print("[bold green]:party_popper: you got it!![/]")
        console_in.print(game_stats.word)
    else:
        if game_stats.remaining_guesses == 0:
            console_in.print("[bold]:disappointed: Sorry, You are out of guesses..[/]")
            console_in.print(game_stats.word)


def keyboard_character_format(keyboard_row:str,
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
                    # Show the keyboard letter as red and struck if the letter was
                    # used and does not appear in the word
                    formatted_char = f"[strike][bold][italics][dark_red]{char}[/][/][/][/]"
                case GuessStatus.WORD_MEMBER:
                    # Show the keyboard letter with yellow highlight if word was used,
                    # is in the word, but has not matched
                    formatted_char = f"{UNMATCHED_BUT_FOUND_STYLE}{char}[/]"
                case GuessStatus.MATCH:
                    # Show the keyboard letter with Green highlight if word was used and is a match
                    formatted_char = f"{MATCHED_STYLE}{char}[/]"
        # Add the styled letter to the total list of letters
        formatted_output.append(formatted_char)
    return " ".join(formatted_output)


def show_keyboard(used_letter_map:dict[str, GuessStatus], console_in):
    """
    Encapsulates the logic to display the used/unused keyboard letters to the user
    Args:
        console_in:  Reference to the Rich Console with which the display shall be printed
        used_letter_map: map of letters used and their context to prior guesses

    """
    console_in.print(keyboard_character_format(QWERTY_TOP, used_letter_map), justify="center")
    console_in.print(keyboard_character_format(QWERTY_MIDDLE, used_letter_map), justify="center")
    console_in.print(keyboard_character_format(QWERTY_BOTTOM, used_letter_map), justify="center")


def refresh_display(console_in):
    """
    Restarts the display anew to show updates to the game (e.g. new results, new input prompts, etc.)
    """
    console_in.clear()
    console_in.rule("[bold blue][blink] :game_die: Hello from Word-all[/blink][/bold blue]")
