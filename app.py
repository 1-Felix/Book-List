import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from modules.goodreads import client

app = Flask(__name__)
gc = client.GoodreadsClient("qkGrXa3h2ICsDDLIkeHsGg", "9JpS3VJ7lo2XEXImBkdnvg6Iz4wDBK0BJUKmdr6DiXk")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set up API
# res = requests.get("https://www.goodreads.com/book/title.json", params={"key": "qkGrXa3h2ICsDDLIkeHsGg", "title": "Eragon"})
# print(res.json())
# res = requests.get("https://www.goodreads.com/book/title.json", params={"key": "qkGrXa3h2ICsDDLIkeHsGg", "title": "eragon"})
# if res.status_code != 200:
#     raise Exception("ERROR: API request unsuccessful.")
# data = res.json()
# print(data)

# bbook = gc.book(isbn="1451648537")
# author = gc.find_author("Christopher")
# print(dir(bbook))
# print("-------Title-------")
# print(bbook.title)
# print("-------ISBN-------")
# print(bbook.isbn)
# print("-------Description-------")
# print(bbook.description)
# print("-------Authors-------")
# print(bbook.authors)
# print("-------Average Rating-------")
# print(bbook.average_rating)
# print("-------image URL-------")
# print(bbook.image_url)
# print("-------link-------")
# print(bbook.link)
# print("-------num pages-------")
# print(bbook.num_pages)
# print("-------small images url-------")
# print(bbook.small_image_url)
# print("-------work-------")
# print(bbook.work)

# print(bbook.cover)


# print(author.books)
# print(bbook.isbn)


@app.route("/")
def index():

    # try:
    # except ValueError:
    #     return render_template("error.html", message="Invalid book number.")
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("index.html", books=books)

@app.route("/books", methods=["POST","GET"])
def books():
    """List all Search Results."""
    book_info = request.form.get("book_id")
    books = db.execute("SELECT * FROM books WHERE title LIKE '%'||:title||'%' OR author LIKE '%'||:author||'%'", {"title": book_info, "author": book_info}).fetchall()

    """Enable Sortinf"""
    sortTitle = db.execute("SELECT * FROM books WHERE title LIKE '%'||:title||'%' OR author LIKE '%'||:author||'%' ORDER BY title", {"title": book_info, "author": book_info}).fetchall()
    sortAuthor = db.execute("SELECT * FROM books WHERE title LIKE '%'||:title||'%' OR author LIKE '%'||:author||'%' ORDER BY author", {"title": book_info, "author": book_info}).fetchall()
    sortYear = db.execute("SELECT * FROM books WHERE title LIKE '%'||:title||'%' OR author LIKE '%'||:author||'%' ORDER BY year", {"title": book_info, "author": book_info}).fetchall()
    sortISBN = db.execute("SELECT * FROM books WHERE title LIKE '%'||:title||'%' OR author LIKE '%'||:author||'%' ORDER BY isbn", {"title": book_info, "author": book_info}).fetchall()

    return render_template("books.html", books=books, sortTitle=sortTitle, sortAuthor=sortAuthor, sortYear=sortYear, sortISBN=sortISBN)

@app.route("/books/<int:book_id>")
def book(book_id):
    """List details about a single book."""

    # Make sure book exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    api_book = gc.book(isbn=book.isbn)
    api_author = api_book.authors[0]
    # print(api_book._author_dict['about'])
    if book is None:
        return render_template("error.html", message="No such book.")

    # Get all passengers.
    # passengers = db.execute("SELECT name FROM passengers WHERE book_id = :book_id",
    #                         {"book_id": book_id}).fetchall()
    # return render_template("book.html", book=book, passengers=passengers)
    return render_template("book.html", book=book, api_book=api_book)

if __name__ == "__main__":
	app.run()
