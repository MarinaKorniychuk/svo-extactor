import logging

import spacy
import itertools
import textacy.extract

from facts.settings import NOT_STOP_WORDS


class SVOExtractor(object):
    """Extract subject-verb-object triples from data."""

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)

        for w in NOT_STOP_WORDS:
            self.nlp.vocab[w].is_stop = False

        self.logger = logging.getLogger("svo-extractor")

    def process(self, data):
        self.logger.info(f"Got data ({len(data)} items) to extract SVO triples")
        self.logger.info(f"Start extracting SVO triples")

        svo_triples = sum((self.process_item(item) for item in data), [])

        self.logger.info(f"Finished extracting SVO triples from data")
        return svo_triples

    def process_item(self, item):
        text_tokens = itertools.chain.from_iterable(
            [sent for sent in self.nlp(item["text"].lower()).sents][:2]
        )

        filtered_tokens = [token.text for token in text_tokens if not token.is_stop]
        filtered_doc = self.nlp(" ".join(w for w in filtered_tokens))

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
