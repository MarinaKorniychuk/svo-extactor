import logging
import re

import numpy as np
from spacy.attrs import POS, SENT_START, LOWER
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc
from spacy.util import filter_spans

TOKENS_TO_FILTER = ("PUNCT", "DET", "PRON", "SPACE", "ADV", "X", "PART", "PROPN", "SYM")

FILTER_ATTRS_TO_EXPORT = [POS, SENT_START]
CROP_ATTRS_TO_EXPORT = [SENT_START]


class MergeTermNamesPipeline(object):
    """Custom pipeline component that merges term names into single token.

    Find matches for term names in doc and merge them into single token
    to make sure term names will be correctly extracted in SVO triples.
    """

    def __init__(self, nlp):
        self.nlp = nlp
        self.logger = logging.getLogger("merge-terms-component")
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab, LOWER)

    def __call__(self, doc):
        matched_phrases = self.phrase_matcher(doc)

        matched_spans = []
        for match_id, start, end in matched_phrases:
            matched_spans.append(doc[start:end])

        filtered_spans = filter_spans(matched_spans)
        with doc.retokenize() as retokenizer:
            for span in filtered_spans:
                attrs = {"tag": span.root.tag, "pos": span.root.pos}
                retokenizer.merge(span, attrs=attrs)

        return doc

    def add_patterns_to_match(self, terms):
        terms = self.extend_terms_list(terms)
        patterns = [
            self.nlp(term, disable=["filter", "merge_chunks"]) for term in terms
        ]
        self.phrase_matcher.add("TN", None, *patterns)

    def extend_terms_list(self, terms):
        new = []
        pattern = r" \(.*\)"
        for term in terms:
            if re.findall(pattern, term):
                new.append(re.sub(pattern, "", term))
        return terms + new


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


def filter_and_merge_num_noun_chunks(doc):
    """Filter overlapping spans and merge not to long NOUN chunks
    that include NUM tokens into a single NOUN token.

    Filter a sequence of spans to remove duplicates or overlaps
    before merging to avoid conflicting merges.
    """
    if not doc.is_parsed:
        return doc

    chunks = doc.noun_chunks
    filtered_chunks = filter_spans(chunks)
    filtered_num_chunks = filter(
        lambda span: len(span) <= 5 and any(t.pos_ is "NUM" for t in span),
        filtered_chunks,
    )
    with doc.retokenize() as retokenizer:
        for ch in filtered_num_chunks:
            # a new token is marked manually as NOUN so that it is not marked as NUM
            attrs = {"tag": ch.root.tag, "dep": ch.root.dep, "pos": "NOUN"}
            retokenizer.merge(ch, attrs=attrs)

    return doc
