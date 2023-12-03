import re

from bs4 import BeautifulSoup

from locators.book_page_locators import BooksPageLocator
from parsers.book import BookParser


class BookPage:
    def __init__(self, page):
        self.soup = BeautifulSoup(page, "html.parser")

    @property
    def books(self):
        locator = BooksPageLocator.BOOK
        book_tags = self.soup.select(locator)
        return [BookParser(e) for e in book_tags]

    @property
    def pages(self):
        locator = BooksPageLocator.PAGER
        pages_tag = self.soup.select_one(locator).string
        pattern = "Page [0-9]+ of ([0-9]+)"
        page_number = re.search(pattern, pages_tag)
        return int(page_number.group(1))
