import random
import json
from pathlib import Path


class Sampler:
    def __call__(self, path):
        choice = str(random.choice(self.word_range))

        sample = [
            {"word": w, "reversed": random.choice([True, False]), "positions": []}
            for w in self.word_list[self.category].get(choice, [])
        ]

        placeables = list(filter(lambda w: w and _filter_criteria(w, path), sample))
        try:
            return random.choice(placeables)
        except Exception:
            return None

    def __init__(self, category, min_length, max_length):
        self.category = category
        self.word_range = range(min_length, max_length + 1)
        self.word_list = _get_word_list()


def _get_word_list():
    # TODO: Find a better way to do this.
    path = Path(__file__).parent / "./wordlist.json"
    with open(path, "r") as infile:
        return json.load(infile)


def _filter_criteria(word_item, path):
    word = word_item["word"]
    word = word[::-1] if word_item["reversed"] else word
    if len(word) > len(path):
        return False

    return _is_placeable(word, path)


def _is_placeable(word, path):
    return not any((step != " " and step != char) for (char, step) in zip(word, path))
