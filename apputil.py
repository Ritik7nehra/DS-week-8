from collections import defaultdict
import numpy as np

class MarkovText(object):

    def __init__(self, corpus):
        self.corpus = corpus
        self.term_dict = None

    def get_term_dict(self):
        """Build transition dictionary for Markov chain text generation."""

        tokens = self.corpus.split()
        term_dict = defaultdict(list)

        # Build transitions
        for i in range(len(tokens) - 1):
            current_token = tokens[i]
            next_token = tokens[i + 1]
            term_dict[current_token].append(next_token)

        self.term_dict = dict(term_dict)
        return self.term_dict

    def generate(self, seed_term=None, term_count=15):
        """Generate text using Markov chain transitions."""

        if self.term_dict is None:
            self.get_term_dict()

        if not self.term_dict:
            raise ValueError("Term dictionary is empty.")

        # Seed term logic
        if seed_term is not None:
            if seed_term not in self.term_dict:
                raise ValueError("Seed term not found in corpus.")
            current = seed_term
        else:
            current = np.random.choice(list(self.term_dict.keys()))

        output = [current]

        for _ in range(term_count - 1):
            if current not in self.term_dict or len(self.term_dict[current]) == 0:
                # If last word has no transitions → choose a new random seed
                current = np.random.choice(list(self.term_dict.keys()))
            else:
                current = np.random.choice(self.term_dict[current])

            output.append(current)

        return " ".join(output)
