import string

from typeguard import typechecked

import random

class RandomHelper:

    @staticmethod
    @typechecked
    def create_random_alphabetic_code(
        number_of_chars: int,
        char_set: set[str] = set(string.ascii_lowercase),
        suppress_print: bool = True) -> str:

        if number_of_chars <= 0:
            raise Exception("The number of characters must be a positive integer")

        if len(char_set) == 0:
            raise Exception("The character set must contain at least 1 element")

        char_set_list: list[str] = list(char_set)
        
        random_chars: list[str] = []

        for _ in range(number_of_chars):

            random_char: str = random.choice(char_set_list) 

            random_chars.append(random_char)
        
        random_alphabetic_code: str = "".join(random_chars)

        if not suppress_print:
            
            print(f"\nRandom alphabetic code: {random_alphabetic_code}")
        
        return random_alphabetic_code

