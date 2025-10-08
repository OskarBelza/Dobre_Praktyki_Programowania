import re


def is_palindrome(text: str) -> bool:
    text = text.lower().strip().replace(" ", "")
    return text == text[::-1]


def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Input should be a non-negative integer")
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def count_vowels(text: str) -> int:
    vowels = "aeiouyąęó"
    text = text.lower()
    return sum(1 for char in text if char in vowels)


def calculate_discount(price: float, discount: float) -> float:
    if discount < 0 or discount > 1:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount)


def flatten_list(nested_list: list) -> list:
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list


def word_frequency(text: str) -> dict:
    word_no_punctuation = re.sub(r'[^\w\s]', '', text)
    word_no_punctuation = word_no_punctuation.lower().split()
    frequency = {}
    for word in word_no_punctuation:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
