import numpy as np
from spacy.attrs import POS, SENT_START
from spacy.tokens import Doc
from spacy.util import filter_spans

TOKENS_TO_FILTER = ("PUNCT", "DET", "ADP", "SPACE", "PRON", "PART", "PROPN")

FILTER_ATTRS_TO_EXPORT = [POS, SENT_START]
CROP_ATTRS_TO_EXPORT = [SENT_START]


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


def filter_and_merge_noun_chunks(doc):
    """Filter overlapping spans and merge noun chunks into a single token.

    Component to replace build-in pipeline component merge_noun_chunks.
    Filter a sequence of spans to remove duplicates or overlaps
    before merging to avoid conflicting merges.
    """
    if not doc.is_parsed:
        return doc

    chunks = doc.noun_chunks
    filtered_chunks = filter_spans(chunks)

    with doc.retokenize() as retokenizer:
        for ch in filtered_chunks:
            attrs = {"tag": ch.root.tag, "dep": ch.root.dep, "pos": ch.root.pos}
            retokenizer.merge(ch, attrs=attrs)

    return doc
