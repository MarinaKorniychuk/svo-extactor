import numpy as np
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA, SENT_START
from spacy.tokens import Doc

from facts.settings import TOKENS_TO_FILTER


def remove_tokens_on_match(doc):
    """Filter out stop word tokens, while maintaining sentences boundaries."""
    indices = []
    for index, token in enumerate(doc):
        if token.pos_ in TOKENS_TO_FILTER:
            indices.append(index)
            if token.is_sent_start:
                doc[index + 1].is_sent_start = True

    np_array = doc.to_array([LOWER, POS, ENT_TYPE, IS_ALPHA, SENT_START])
    np_array = np.delete(np_array, indices, axis=0)
    words = [t.text for i, t in enumerate(doc) if i not in indices]
    doc2 = Doc(doc.vocab, words=words)
    doc2.from_array([LOWER, POS, ENT_TYPE, IS_ALPHA, SENT_START], np_array)
    return doc2


def crop_to_two_sentences(doc):
    """Crop the text to two or fewer sentences."""
    np_array = doc.to_array(SENT_START)
    sent_start_indices = np.where(np_array == 1)[0]

    if len(sent_start_indices) > 2:
        fragment_len = sent_start_indices[2]
    else:
        fragment_len = len(np_array)

    words = [t.text for i, t in enumerate(doc[:fragment_len])]
    doc2 = Doc(doc.vocab, words=words)
    doc2.from_array(SENT_START, np_array[:fragment_len])
    return doc2
