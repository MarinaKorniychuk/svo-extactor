import logging
from typing import Iterable

import spacy
import itertools
import textacy.extract

from facts.settings import NOT_STOP_WORDS


class SVOExtractor(object):
    """Extract subject-verb-object triples from data."""

    def __init__(self):
        """Load and initialize spacy 'en' model,
        add built-in pipeline component Sentencizer for sentence segmentation.
        Update model's default list of stop words by removing words from NOT_STOP_WORDS list.
        """
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)

        for w in NOT_STOP_WORDS:
            self.nlp.vocab[w].is_stop = False

        self.logger = logging.getLogger("svo-extractor")

    def process(self, data: Iterable) -> list:
        """Call extracting SVO triples for each item in the data and aggregate the results."""
        self.logger.info(f"Got data ({len(data)} items) to extract SVO triples")
        self.logger.info(f"Start extracting SVO triples")

        svo_triples = sum((self.process_item(item) for item in data), [])

        self.logger.info(f"Finished extracting SVO triples from data")
        return svo_triples

    def process_item(self, item: dict) -> list:
        """Use nlp spacy model to get 2 first sentences from the full definition.
        Filter stop words and extract SVO triples.
        For each SVO create dict with the following data:

        - name of the term being defined
        - subject of the SVO triple
        - verb of the SVO triple
        - object of the SVO triple
        - URL of the definition page
        - the original full text of the definition
        """
        sentences = [sent for sent in self.nlp(item["text"].lower()).sents][:2]
        text_tokens = itertools.chain.from_iterable(sentences)

        filtered_text = [token.text for token in text_tokens if not token.is_stop]
        filtered_doc = self.nlp(" ".join(w for w in filtered_text))

        svo_triples = []
        for svo in textacy.extract.subject_verb_object_triples(filtered_doc):
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
