from pathlib import Path

from common.tests import spider
from facts.spiders import BlacksLawSpider


class BlacksLawSpiderTestCase(spider.SpiderTestCase):

    callback = BlacksLawSpider.parse_detail
    response_html = Path.joinpath(
        Path(__file__).parent, "responses", f"{BlacksLawSpider.name}/detail.html"
    )
    url = "https://thelawdictionary.org/data-processing-insurance"

    def get_local_response(self):
        response = super().get_local_response()
        response.meta["title"] = "data processing insurance"
        return response

    def check_results(self, results):
        self.assertEqual(1, len(results))

        item = results[0]
        self.assertEqual(
            "https://thelawdictionary.org/data-processing-insurance", item["url"]
        )
        self.assertEqual("data processing insurance", item["title"])
        self.assertEqual(
            "Protection against loss of equipment and media used in data processing. It also "
            "helps with restarting business operations. It is in the specified risk or "
            "hazards that the items covered are listed.",
            item["text"],
        )
