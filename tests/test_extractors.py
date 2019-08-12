from unittest import TestCase

from facts.extractors import SVOExtractor

data = [
    {
        "title": "Financial Accounting",
        "text": "Financial accounting is the process of recording, summarizing and reporting the myriad of "
        "transactions resulting from business operations over a period of time. These transactions are "
        "summarized in the preparation of financial statements, including the balance sheet, income statement "
        "and cash flow statement, that record the company's operating performance over a specified period.",
        "url": "https://www.investopedia.com/terms/f/financialaccounting.asp",
    },
    {
        "title": "Balance Sheet Reserves",
        "text": "Balance sheet reserves refer to the amount expressed as a liability on the insurance "
        "company's balance sheet for benefits owed to policy owners. Balance sheet reserves represent "
        "the amount of money insurance companies set aside for future insurance claims or claims that "
        "have been filed but not yet reported to the insurance company or settled. The levels of "
        "balance sheet reserves to be maintained is regulated by law.",
        "url": "https://www.investopedia.com/terms/b/balance-sheet-reserves.asp",
    },
]


class ExtractorSVOTestCase(TestCase):
    def setUp(self):
        self.extractor = SVOExtractor()

    def test_svo_extraction(self):
        keys = ["page", "subject", "verb", "object", "url"]
        svo_triples = self.extractor.process(data)
        for svo in svo_triples:
            for key in keys:
                self.assertIn(key, svo)

    def test_empty_data(self):
        empty_data = []
        svo_triples = self.extractor.process(empty_data)
        self.assertEqual(svo_triples, [])
