import math
import re


class OldScratchcard:
    winning_numbers: list[int]
    my_numbers: list[int]

    def __init__(self, raw_card: str) -> None:
        """
        Example:
            >>> card = OldScratchcard("Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53")
            >>> card.winning_numbers
            >>> [41, 48, 83, 86, 17]
            >>> card.my_numbers
            >>> [83, 86, 6, 31, 17, 9, 48, 53]
        """
        card_with_prefix_removed = re.sub(r"Card.*[\d+]: ", "", raw_card)
        raw_winning_numbers, raw_my_numbers = card_with_prefix_removed.split("|")
        self.winning_numbers = [int(number) for number in raw_winning_numbers.split(" ") if number]
        self.my_numbers = [int(number) for number in raw_my_numbers.split(" ") if number]

    @property
    def value(self) -> int:
        winning_numbers = set.intersection(set(self.winning_numbers), self.my_numbers)
        return int(math.pow(2, len(winning_numbers) - 1))


class Scratchcard:
    card_number: int
    winning_numbers: list[int]
    my_numbers: list[int]

    _raw_card: str  # so we can easily compare objects

    def __init__(self, raw_card: str) -> None:
        """
        Example:
            >>> ❯ card = Scratchcard("Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53")
            >>> ❯ card.card_number
            >>> 1
            >>> ❯ card.winning_numbers
            >>> [41, 48, 83, 86, 17]
            >>> ❯ card.my_numbers
            >>> [83, 86, 6, 31, 17, 9, 48, 53]
        """
        self._raw_card = raw_card
        self.card_number = int(re.findall(r"Card\s+(\d+):[\d|\s|\|]+", raw_card)[0])
        card_with_prefix_removed = re.sub(r"Card.*[\d+]: ", "", raw_card)
        raw_winning_numbers, raw_my_numbers = card_with_prefix_removed.split("|")
        self.winning_numbers = [int(number) for number in raw_winning_numbers.split(" ") if number]
        self.my_numbers = [int(number) for number in raw_my_numbers.split(" ") if number]

    def __repr__(self):
        return f"Scratchcard({self._raw_card})"

    def __hash__(self) -> int:
        return hash(self._raw_card)

    @property
    def value(self) -> int:
        # The value has changed from 2^x to x
        winning_numbers = set.intersection(set(self.winning_numbers), self.my_numbers)
        return len(winning_numbers)


def get_value_of_old_scratchcards(raw_scratchcards: str) -> int:
    return sum(
        OldScratchcard(raw_scratchcard).value
        for raw_scratchcard in raw_scratchcards.split("\n")
        if raw_scratchcard != "" and not raw_scratchcard.isspace()
    )


class Cards:
    original_cards: set[Scratchcard]
    original_card_mapping: dict[int, Scratchcard]

    final_count: int

    def __init__(self, raw_scratchcards: str) -> None:
        self.original_cards = {
            Scratchcard(raw_scratchcard)
            for raw_scratchcard in raw_scratchcards.split("\n")
            if raw_scratchcard != "" and not raw_scratchcard.isspace()
        }
        self.original_card_mapping = {
            scratchcard.card_number: scratchcard
            for scratchcard in self.original_cards
        }

    @property
    def final_count(self):
        final_cards = self.process_scratchcards(self.original_cards)
        return len(final_cards)

    def get_freebie_cards(self, scratchcard: Scratchcard) -> set[Scratchcard]:
        card_number = int(scratchcard.card_number)
        card_value = int(scratchcard.value)

        freebie_card_numbers = list(range(card_number + 1, card_number + card_value + 1))
        return {self.original_card_mapping[freebie_card_number] for freebie_card_number in freebie_card_numbers}

    def process_scratchcards(self, scratchcards: set[Scratchcard]) -> list[Scratchcard]:
        """Returns the final scratchcards obtained after processing each one in the given set

        Note:
            - will use recursion so start with the end case + work backwards
        """
        final_cards = []
        for scratchcard in scratchcards:
            match scratchcard.value:
                case 0:
                    final_cards.append(scratchcard)
                case _:
                    final_cards.extend(
                        [scratchcard] +
                        self.process_scratchcards(
                            self.get_freebie_cards(scratchcard),
                        )
                    )

        return final_cards


def get_final_count_of_scratchcards(raw_scratchcards: str) -> int:
    return Cards(raw_scratchcards).final_count
