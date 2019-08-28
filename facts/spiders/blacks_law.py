import scrapy


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

        for detail_link in response.css(".type-post a"):
            yield response.follow(url=detail_link, callback=self.parse_detail)

        next_page_url = response.css("a.next::attr(href)").get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_list)

    def parse_detail(self, response):
        """Parse a response from term Detail page."""
        if not response.css("h1.title b"):
            self.logger.warning(
                f"No definition for a term from <GET {response.url}>: SKIPPING"
            )
            return

        text = "".join(response.css(".entry p")[0].css("*::text").getall())
        yield {
            "url": response.url,
            "title": response.css("h1.title b::text").get().lower().strip(),
            "text": text.replace("\xa0", " ").strip(),
        }
