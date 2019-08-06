from scrapy.crawler import CrawlerRunner
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
from twisted.internet import defer
from unittest import SkipTest, TestCase

from common.tests import get_class_from_method, fake_response_from_file


class SpiderTestCase(TestCase):
    """Base TestCase class for testing Spider classes."""

    callback = None
    response_html = None
    url = None
    request_cls = Request
    request_args = {}

    def setUp(self):
        self.spider_class = get_class_from_method(self.callback)
        self.spider = self.spider_class()

    def check_results(self, results):
        pass

    def check_results_local(self, results):
        self.check_results(results)

    def check_results_remote(self, results):
        self.check_results(results)

    def get_local_response(self):
        return fake_response_from_file(self.response_html, self.url)

    def get_callback(self):
        return getattr(self.spider_class, self.callback.__name__)

    def test_callback_local(self):
        """Test callback with locally stored response."""
        if not self.response_html:
            raise SkipTest("No HTML provided")

        callback = self.get_callback()
        results = list(callback(self.spider, self.get_local_response()))

        self.check_results_local(results)

    @defer.inlineCallbacks
    def test_callback_remote(self):
        """Test callback with dynamically fetched response."""
        if not self.url:
            raise SkipTest("No URL provided")

        results = []
        callback = self.get_callback()

        def callback_wrapper(response):
            result = callback(self.spider, response)
            results.extend(list(result))
            yield from result

        request = self.request_cls(self.url, callback_wrapper, **self.request_args)
        self.spider_class.start_requests = lambda s: [request]

        runner = CrawlerRunner({**get_project_settings(), "LOG_LEVEL": "ERROR"})
        yield runner.crawl(self.spider_class)
        self.check_results_remote(results)
