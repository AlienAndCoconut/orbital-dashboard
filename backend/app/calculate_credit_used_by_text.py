import re
from decimal import Decimal

TEXT_BASE_COST = Decimal(1)
CHARACTER_COST = Decimal(0.05)
WORD_LENGTH_COST = (Decimal(0.1), Decimal(0.2), Decimal(0.3))
THIRD_VOWELS_COST = Decimal(0.3)
EXCEED_HUNDRED_CHARACTERS_COST = Decimal(5)
UNIQUE_WORD_DEDUCTION = Decimal(2)
PALINDROME_MULTIPLIER_COST = Decimal(2)

vowels_set = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}

def calculate_credit_used_by_text(text: str) -> Decimal:
    total_character_cost = len(text) * CHARACTER_COST
    word_length_cost = get_word_length_cost(text)
    third_vowels_cost = get_third_vowels_cost(text)
    length_penalty_cost = EXCEED_HUNDRED_CHARACTERS_COST if len(text) > 100 else 0
    unique_words_deduction = UNIQUE_WORD_DEDUCTION if is_all_words_unique(text) else 0

    total_cost = (total_character_cost + word_length_cost + third_vowels_cost + length_penalty_cost) - unique_words_deduction

    # The cost will alway be at least base cost.
    # In case it goes lower - we default it to the base cost e.g 1""
    if total_cost <= 0:
        total_cost = TEXT_BASE_COST
    else:
        total_cost += TEXT_BASE_COST

    if is_palindrome(text):
        total_cost *= PALINDROME_MULTIPLIER_COST

    return total_cost.quantize(Decimal('0.01')) # return cost rounded to 2 decimal places


def get_word_length_cost(text: str) -> Decimal:
    """
    Calculates the bonus cost based on the length of words in the text.
    A word is defined as a sequence of letters, plus ' and -.
    """
    words = text.split()
    cost = Decimal(0)

    for word in words:
        # We need to remove special charactersa such as full stops or question mark
        # so it doesn't include as the length of the word.
        filtered_word = re.sub(r"[^a-zA-Z'-]", "", word)
        word_length = len(filtered_word)
        if 1 <= word_length <= 3:
            cost += WORD_LENGTH_COST[0]
        elif 4 <= word_length <= 7:
            cost += WORD_LENGTH_COST[1]
        elif word_length >= 8:
            cost += WORD_LENGTH_COST[2]
        else:
            cost += 0
    
    return cost.quantize(Decimal('0.01'))

def get_third_vowels_cost(text: str) -> Decimal:
    """
    Calculates the cost for every third chracter to see if its an upercase or Lowercase vowel.
    Example: "This one" -> i is the third vowel, so cost += 0.3 and "o" (Note: we count space as character)
    """
    cost = Decimal(0)
    third_vowels_counter = 1
    for char in text:
        if third_vowels_counter % 3 == 0 and char in vowels_set:
            cost += THIRD_VOWELS_COST
        third_vowels_counter += 1
    return cost.quantize(Decimal('0.01'))


def is_all_words_unique(text: str) -> bool:
    """
    Checks if all words in the text are unique (case-sensitive).
    Example: "Hello hello" -> True, "Hello Hello" -> False.
    """
    words = text.split()
    unique_word_set = set()

    for word in words:
        filtered_word = re.sub(r"[^a-zA-Z'-]", "", word)
        if filtered_word in unique_word_set:
            return False
        unique_word_set.add(filtered_word)
    return True


def is_palindrome(text: str) -> bool:
    """
    Checks if a given text is palindrome, ignoring case and non-alphanumeric characters.
    Example: L.eve@l -> level is a palindrome.
    """
    alphanumeric_only_text = "".join([char.lower() if char.isalnum() else "" for char in text])
    return alphanumeric_only_text == alphanumeric_only_text[::-1]