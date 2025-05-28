from decimal import Decimal
import pytest
from app.calculate_credit_used_by_text import (calculate_credit_used_by_text,
                                               get_third_vowels_cost,
                                               get_word_length_cost,
                                               is_all_words_unique,
                                               is_palindrome)


@pytest.mark.parametrize(
    "text, expected_cost",
    [
        ("", Decimal(0)),
        ("a", Decimal('0.10')),
        ("abcdefg", Decimal('0.20')),
        ("one four seventeen", Decimal('0.60')),
    ],
)
def test_get_word_length_cost(
    text, expected_cost
):
    cost = get_word_length_cost(text)
    assert cost == expected_cost

@pytest.mark.parametrize(
    "text, expected_cost",
    [
        ("", 0),
        ("a", 0),
        ("this one", Decimal('0.6')) # 'i' and 'o' are the third vowels
    ],
)
def test_get_third_vowels_cost(text, expected_cost):
    cost = get_third_vowels_cost(text)
    assert cost == expected_cost


@pytest.mark.parametrize(
    "text, is_unique",
    [
        ("hello HELLO", True),
        ("hello hello?", False), # We don't count the question mark as part of the word
        ("That's right, but that's part of the plan", True), # That's and that's are considered different words case-sensitively
    ],
)
def test_is_all_words_unique(text, is_unique):
    are_words_unique = is_all_words_unique(text)
    assert are_words_unique == is_unique


@pytest.mark.parametrize(
    "text, expected_is_palindrome",
    [
        ("", True),  # empty string is considered a palindrome
        ("a", True),
        ("L.eve@l", True),  # level is a palindrome
        ("Hello", False),
        ("A man, a plan, a canal, Panama", True),  # ignoring case and non-alphanumeric characters
    ],
)
def test_is_palindrome(text, expected_is_palindrome):
    is_text_palindrome = is_palindrome(text)
    assert is_text_palindrome == expected_is_palindrome


@pytest.mark.parametrize(
    "text, expected_credit_used",
    [
        ("Are there any restrictions on alterations or improvements?", Decimal('5.20')),
        ("What happens if the property is sold during the lease term?", Decimal('7.05')),
        ("", 2), #  TEXT_BASE_COST * PALINDROME_MULTIPLIER_COST
    ],
)
def test_calculate_credit_used_by_text(text, expected_credit_used):
    cost = calculate_credit_used_by_text(text)
    assert cost == expected_credit_used