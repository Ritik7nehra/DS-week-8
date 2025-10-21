import random
from markov_text import MarkovText

def test_get_term_dict_basic():
    corpus = "Astrid is very kind, is she not?"
    mt = MarkovText(corpus)
    td = mt.get_term_dict()
    assert "is" in td
    assert "very" in td["is"] or "she" in td["is"]

def test_generate_seed():
    random.seed(0)
    corpus = "hello world hello there"
    mt = MarkovText(corpus)
    out = mt.generate(4, seed_term="hello")
    assert isinstance(out, str)
