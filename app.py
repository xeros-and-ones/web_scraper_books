import asyncio
import os

import aiohttp
import requests

from pages.book_pages import BookPage
from utils import database as db

loop = asyncio.get_event_loop()


page_content = requests.get("http://books.toscrape.com").content
page = BookPage(page_content)


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def queue_pages(loop, *urls):
    tasks = []
    async with aiohttp.ClientSession(loop=loop) as session:
        for url in urls:
            tasks.append(fetch_page(session, url))
        queued_pages = asyncio.gather(*tasks)
        return await queued_pages


urls = [
    f"http://books.toscrape.com/catalogue/page-{page_num+1}.html"
    for page_num in range(1, page.pages)
]

pages = loop.run_until_complete(queue_pages(loop, *urls))

books = page.books
for page_content in pages:
    page = BookPage(page_content)
    books.extend(page.books)


def main():
    if not os.path.isfile("books.db"):
        print("database not found... creating one")
        db.create_table()
    else:
        print("database found")
    for book in books:
        dictionary = {"Title": book.title, "Price": book.price, "Availability": book.available}
        db.add(book.title, book.price, book.available)
        print(dictionary)


if __name__ == "__main__":
    main()
