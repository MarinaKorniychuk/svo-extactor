from unittest import TestCase

import pytest
import spacy

from facts.extractors.components import remove_tokens_on_match, crop_to_two_sentences, IS_STOP

LONG_TEXT = (
    "3c1 refers to a portion of the investment company act of 1940 that allows private funds to "
    "avoid the requirements of the securities and exchange commission (sec). 3c1 is shorthand for "
    "the 3(c)(1) exemption found in section 3 of the act. A 52-week high/low is the highest and "
    "lowest price at which a stock has traded during the previous year. It is a technical "
    "indicator used by some traders and investors who view the 52-week high or low as an important "
    "factor in determining a stock's current value and predicting future price movement."
)
SHORT_TEXT = (
    "An abandonment clause in a property insurance contract, under certain circumstances, permits the "
    "property owner to abandon owner's lost or damaged property and still claim a full settlement amount."
)


class TestCropTo2Sentences(TestCase):
    def setUp(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)

    def test_crop_long_text_to_two_sentences(self):
        doc = self.nlp(LONG_TEXT)
        self.assertEqual(len([sent for sent in doc.sents]), 4)

        crop_doc = crop_to_two_sentences(doc)
        self.assertEqual(len([sent for sent in crop_doc.sents]), 2)

    def test_crop_do_not_modify_short_text(self):
        doc = self.nlp(SHORT_TEXT)
        self.assertEqual(len([sent for sent in doc.sents]), 1)

        crop_doc = crop_to_two_sentences(doc)
        self.assertEqual(crop_doc, doc)
        self.assertEqual(len([sent for sent in crop_doc.sents]), 1)


class TestFilteringStopTokens(TestCase):
    def setUp(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)
        self.nlp.add_pipe(remove_tokens_on_match, name="filter", after="tagger")

    def test_filtering_keep_sentence_boundaries_set(self):
        doc = self.nlp(LONG_TEXT, disable=["filter"])
        self.assertEqual(len([sent for sent in doc.sents]), 4)

        filtered_doc = self.nlp(LONG_TEXT)
        self.assertEqual(len([sent for sent in filtered_doc.sents]), 4)

    def test_remove_stop_tokens(self):
        filtered_doc = self.nlp(LONG_TEXT)
        for token in filtered_doc:
            self.assertFalse(IS_STOP(token))
