import scrapy


class InvestopediaSpider(scrapy.Spider):
    """Crawl data from Investopedia (https://www.investopedia.com/) Dictionary.
    Start with initial request to Home page and navigate to list of terms for each extracted symbol in dictionary.
    Send request to Detail page for each term in the list and extract the following data:

    - the title of the page
    - the first paragraph of the page
    - the URL of the page
    """

    name = "investopedia"
    allow_domains = ["investopedia.com"]
    start_urls = ["https://www.investopedia.com/"]

    def parse(self, response):
        """ Parse a response from Home page."""
        for link in response.css("li.terms-bar__item a"):
            yield response.follow(url=link, callback=self.parse_list)

    def parse_list(self, response):
        """Parse a response from Terms Beginning With "[symbol]" page."""
        for detail_link in response.css(".dictionary-listing a"):
            yield response.follow(url=detail_link, callback=self.parse_detail)

    def parse_detail(self, response):
        """Parse a response from term Detail page."""
        text = "".join(response.css(".article-body p")[0].css("p *::text").getall())
        yield {
            "url": response.url,
            "title": response.css("h1.article-heading::text").get().strip(),
            "text": text.replace("\xa0", " ").strip(),
        }
