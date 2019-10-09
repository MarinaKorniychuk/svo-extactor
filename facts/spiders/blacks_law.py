import scrapy

from common.utils import remove_html_markups


class BlacksLawSpider(scrapy.Spider):
    """Crawl data from The Law Dictionary (https://thelawdictionary.org/).
    Start with initial request to Home page and navigate to list of terms for each extracted symbol in dictionary.
    Send request to Detail page for each term in the list and extract the following data:

    - the title of the page
    - the first paragraph of the page
    - the URL of the page
    """

    name = "blacks_law"
    allow_domains = ["thelawdictionary.org"]
    start_urls = ["https://thelawdictionary.org/"]

    def parse(self, response):
        for link in response.css("li.menu-item-object-category a"):
            yield response.follow(url=link, callback=self.parse_list)

    def parse_list(self, response):
        """Parse a response from "Archive | [symbol]" page."""

        for detail_link in response.css(".type-post a[title]"):
            yield response.follow(
                url=detail_link,
                callback=self.parse_detail,
                meta={"title": detail_link.attrib["title"]},
            )

        next_page_url = response.css("a.next::attr(href)").get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_list)

    def parse_detail(self, response):
        """Parse a response from term Detail page."""
        if not response.xpath('.//div[contains(text(), "Link to This Definition")]'):
            self.logger.warning(
                f"No definition for a term from <GET {response.url}>: SKIPPING"
            )
            return

        html = response.css(".entry p")[0].get().split("<!--")[0]
        text = remove_html_markups(html)

        yield {
            "url": response.url,
            "title": response.meta["title"].replace("\n", " ").lower(),
            "text": text.replace("\xa0", " ").replace("\n", " ").strip(),
        }
