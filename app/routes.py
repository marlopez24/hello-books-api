
from os import abort
from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")
authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))

    return book

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))



# created a post for only author
@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)


# Helper function to get the valid input for author  that we will use in the new nested routes
def validate_author(author_id):
    try:
        author_id = int(author_id)
    except:
        abort(make_response({"message":f"author {author_id} invalid"}, 400))

    author = Author.query.get(author_id)

    if not author:
        abort(make_response({"message":f"author {author_id} not found"}, 404))

    return author

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_author(author_id)

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=author
    )
    db.session.add(new_book)
    db.session.commit()
    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)


#nested route reading books and getting the author which is the parent
@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books(author_id):

    author = validate_author(author_id)

    books_response = []
    for book in author.books:
        books_response.append(
            {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }
        )
    return jsonify(books_response), 200


#getting a single author database to read all authors
@authors_bp.route("", methods=["GET"])
def read_all_authors():
    authors = Author.query.all()

    authors_response = []
    for author in authors:
        authors_response.append(
            {
                "name": author.title
            }
        )
    return jsonify(authors_response), 200 