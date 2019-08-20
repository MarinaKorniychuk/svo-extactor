import numpy as np
from spacy.tokens import Doc

from facts.settings import (
    TOKENS_TO_FILTER,
    FILTER_ATTRS_TO_EXPORT,
    CROP_ATTRS_TO_EXPORT,
)


def remove_tokens_on_match(doc):
    """Filter out stop word tokens, while maintaining sentences boundaries.

    Note: should be added to pipeline after tagger, but before parser component."""
    indices = []
    for index, token in enumerate(doc):
        if token.pos_ in TOKENS_TO_FILTER:
            indices.append(index)
            if token.is_sent_start and len(doc) > index + 1:
                doc[index + 1].is_sent_start = True

    np_array = doc.to_array(FILTER_ATTRS_TO_EXPORT)
    np_array = np.delete(np_array, indices, axis=0)
    words = [t.text for i, t in enumerate(doc) if i not in indices]
    doc2 = Doc(doc.vocab, words=words)
    doc2.from_array(FILTER_ATTRS_TO_EXPORT, np_array)
    return doc2


def crop_to_two_sentences(doc):
    """Crop the text to two sentences.
    Do not affect doc if there are only two or fewer sentences.

    Note: should be added to pipeline after sentencizer,
    so that sentence boundaries are already set, but before parser component."""
    np_array = doc.to_array(CROP_ATTRS_TO_EXPORT)
    sent_start_indices = np.where(np_array == 1)[0]

    if len(sent_start_indices) <= 2:
        return doc

    fragment_len = sent_start_indices[2]
    words = [t.text for i, t in enumerate(doc[:fragment_len])]
    doc2 = Doc(doc.vocab, words=words)
    doc2.from_array(CROP_ATTRS_TO_EXPORT, np_array[:fragment_len])
    return doc2
