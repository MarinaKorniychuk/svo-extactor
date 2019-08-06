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
        for link in response.css("#terms-bar__list_1-0 a"):
            yield response.follow(url=link, callback=self.parse_list)

    def parse_list(self, response):
        """Parse a response from Terms Beginning With "[symbol]" page."""
        for detail_link in response.css("li.item a"):
            yield response.follow(url=detail_link, callback=self.parse_detail)

        next_page_url = response.css("li.next a::attr(href)").get()

        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse_list)

    def parse_detail(self, response):
        """Parse a response from term Detail page."""
        # There are some terms in the dictionary for which Detail page does not exist,
        # Request like this are redirected to other pages (e.g Investing Essentials)
        if response.meta.get("redirect_urls"):
            self.logger.warning(
                f'Redirected (301) from <GET {response.url}> to <GET {response.meta["redirect_urls"][0]}>: SKIPPING'
            )
            return

        yield {
            "page_url": response.url,
            "page_title": response.css("h1#article-heading_2-0::text").get().strip(),
            "text": "".join(
                response.css("#article-body_1-0 p")[0].css("p *::text").getall()
            ).strip(),
        }
