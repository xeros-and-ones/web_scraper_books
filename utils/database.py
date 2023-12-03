from typing import Dict, List, Union

from utils.database_connection import DatabaseConnection

Book = Dict[str, Union[str, int]]


if __name__ == "__main__":
    print("this is not supposed to be run: something wrong happened ")
    exit()


def create_table() -> None:
    with DatabaseConnection("books.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Books(title text primary key, price integer, availability)"
        )


def add(book_title: str, price: int, availability: bool) -> None:
    with DatabaseConnection("books.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO Books VALUES(?, ?, ?)", (book_title, price, availability)
        )


def list_books() -> List[Book]:
    with DatabaseConnection("books.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Books")
        books = [
            {"title": row[0], "price": row[1], "availability": row[2]} for row in cursor.fetchall()
        ]
    return books
