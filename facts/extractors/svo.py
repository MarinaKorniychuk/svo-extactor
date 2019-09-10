import logging
from typing import Iterable

import spacy
import textacy.extract

from facts.extractors.components import (
    crop_to_two_sentences,
    remove_tokens_on_match,
    filter_and_merge_num_noun_chunks,
    MergeTermNamesPipeline,
)


class SVOExtractor(object):
    """Extract subject-verb-object triples from data."""

    def __init__(self):
        """Load and initialize spacy 'en' model,
        add built-in pipeline components for sentence segmentation and merging noun chunks,
        also add to pipeline custom components to crop the paragraph and filter stop words.

        Components' order in the pipeline is the following:
        ['sentencizer', 'crop', 'tagger', 'filter', 'parser', 'merge_num_chunks']
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)

        # add custom components to pipeline
        self.nlp.add_pipe(crop_to_two_sentences, name="crop", after="sentencizer")
        self.nlp.add_pipe(remove_tokens_on_match, name="filter", after="tagger")
        self.nlp.add_pipe(filter_and_merge_num_noun_chunks, name="merge_num_chunks")

        self.nlp.remove_pipe("ner")

        self.logger = logging.getLogger("svo-extractor")

    def add_merge_terms_pipeline(self, terms):
        """Add TermNamesPipeline component to nlp model."""
        merge_term_names = MergeTermNamesPipeline(self.nlp)
        merge_term_names.add_patterns_to_match(terms)

        self.nlp.add_pipe(merge_term_names, name="merge_terms", after="tagger")

    def process(self, data: Iterable) -> list:
        """Call extracting SVO triples for each item in the data and aggregate the results."""
        self.logger.info(f"Got data ({len(data)} items) to extract SVO triples")
        self.logger.info(f"Start extracting SVO triples")

        terms = [i["title"].lower() for i in data]
        self.add_merge_terms_pipeline(terms)

        svo_triples = sum((self.process_item(item) for item in data), [])

        self.logger.info(f"Finished extracting SVO triples from data")
        return svo_triples

    def process_item(self, item: dict) -> list:
        """Run the text through nlp spacy model to extract SVO triples.
        For each SVO create dict with the following data:

        - name of the term being defined
        - subject of the SVO triple
        - verb of the SVO triple
        - object of the SVO triple
        - URL of the definition page
        - the original full text of the definition
        """
        text = item["text"].replace("“", '"').replace("”", '"').lower()
        doc = self.nlp(text)

        svo_triples = []
        for svo in textacy.extract.subject_verb_object_triples(doc):
            if svo[0].root.pos_ == "VERB" or svo[2].root.pos_ == "VERB":
                continue
            svo_triples.append(
                {
                    "name": item["title"],
                    "subject": svo[0].lemma_,
                    "verb": svo[1].lemma_,
                    "object": svo[2].lemma_,
                    "url": item["url"],
                    "definition": item["text"],
                }
            )

        return svo_triples
