from pathlib import Path

from common.tests import spider
from facts.spiders import InvestopediaSpider


class InvestopediaSpiderTestCase(spider.SpiderTestCase):

    callback = InvestopediaSpider.parse_detail
    response_html = Path.joinpath(
        Path(__file__).parent, "responses", f"{InvestopediaSpider.name}/detail.html"
    )
    url = "https://www.investopedia.com/terms/t/takeabath.asp"

    def check_results(self, results):
        self.assertEqual(1, len(results))

        item = results[0]
        self.assertEqual(
            "https://www.investopedia.com/terms/t/takeabath.asp", item["url"]
        )
        self.assertEqual("Take a Bath", item["title"])
        self.assertEqual(
            "Take a bath is a slang term that refers to an investor who has experienced a significant loss from "
            "an investment. Investors whose shares have declined substantially are said to have taken a bath. For "
            "example, during the Great Recession between 2007 and 2009, or the crash of technology stocks in early "
            "2000, many investors, because of their large losses, were said to have taken a bath.",
            item["text"],
        )
