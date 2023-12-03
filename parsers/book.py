import re

from locators.book_locators import BookLocator


class BookParser:
    """
    takes in a single quote div and outputs the Content, Author and Tags
    """

    def __init__(self, parent):
        self.parent = parent

    def __repr__(self):
        return f"Quote: {self.title} \nPrice: {self.price}\nAvailability: {self.available}\n"

    @property
    def title(self):
        locator = BookLocator.TITLE
        return self.parent.select_one(locator).attrs["title"]

    @property
    def price(self):
        locator = BookLocator.PRICE
        price = self.parent.select_one(locator).string
        pattern = "[0-9]+\.[0-9]+"
        price_re = re.search(pattern, price)
        return float(price_re.group(0))

    @property
    def available(self):
        locator = BookLocator.AVAILABILITY
        if self.parent.select_one(locator).text.strip() == "In stock":
            return True
        else:
            return False
