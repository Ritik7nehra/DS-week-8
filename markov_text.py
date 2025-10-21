"""
markov_text.py

Simple first-order Markov text generator for Week 8 exercise.
"""

from collections import defaultdict
import random
from typing import Dict, List, Optional


class MarkovText:
    """A simple first-order Markov text generator."""

    def __init__(self, corpus: str):
        """
        Initialize with a cleaned corpus string.
        Tokenization is whitespace-based (split()) by default.
        """
        if not isinstance(corpus, str):
            raise TypeError("corpus must be a string")
        self.corpus = corpus.strip()
        self.tokens = self._tokenize(self.corpus)
        self.term_dict: Dict[str, List[str]] = {}
        if self.tokens:
            self.get_term_dict()

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """
        Tokenize text by whitespace.
        """
        if text == "":
            return []
        return text.split()

    def get_term_dict(self) -> Dict[str, List[str]]:
        """
        Build and return the term dictionary:
        key -> token (string)
        value -> list of tokens that follow the key in the corpus.
        Duplicates are included to reflect empirical frequency.
        """
        term_dict: Dict[str, List[str]] = defaultdict(list)

        # Record follower tokens for each token occurrence
        for i in range(len(self.tokens) - 1):
            current_token = self.tokens[i]
            next_token = self.tokens[i + 1]
            term_dict[current_token].append(next_token)

        # Ensure every token appears as a key, even if no followers
        for token in self.tokens:
            term_dict.setdefault(token, [])

        # Save and return as plain dict
        self.term_dict = dict(term_dict)
        return self.term_dict

    def generate(
        self, term_count: int = 20, seed_term: Optional[str] = None
    ) -> str:
        """
        Generate text with the Markov property:
        - term_count: maximum number of tokens to produce (int > 0)
        - seed_term: optional starting token; if provided and not in corpus -> ValueError

        If the current token has no followers, generation stops early.
        Returns a string joined by spaces.
        """
        if term_count <= 0:
            raise ValueError("term_count must be a positive integer")

        if not self.term_dict:
            return ""

        # validate seed
        if seed_term is not None:
            if seed_term not in self.term_dict:
                raise ValueError(f"seed_term '{seed_term}' not found in corpus")
            current = seed_term
        else:
            current = random.choice(list(self.term_dict.keys()))

        output_tokens = [current]

        for _ in range(term_count - 1):
            followers = self.term_dict.get(current, [])
            if not followers:
                # stop early if no followers
                break
            next_token = random.choice(followers)
            output_tokens.append(next_token)
            current = next_token

        return " ".join(output_tokens)
