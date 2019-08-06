from scrapy.http import HtmlResponse, Request


def fake_response_from_file(file_path, url=None):
    """
    Create a Scrapy fake HTTP response from a HTML file
    @param file_path: The absolute path to response HTML file.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = "http://www.example.com"

    request = Request(url=url)

    with open(file_path, "r") as file:
        response = HtmlResponse(
            url=url, request=request, body=file.read(), encoding="utf-8"
        )
    return response


def fake_response_redirect(url=None):
    """
    Create a Scrapy fake HTTP response after redirect from requested url to another one.
    @param url: The URL of the response.
    returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = "http://www.example.com"

    request = Request(url=url)

    response = HtmlResponse(url=url, request=request, body="", encoding="utf-8")
    response.meta["redirect_urls"] = "http://www.redirect-url.com"

    return response
