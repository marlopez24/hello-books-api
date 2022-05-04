from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request, abort

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

#helper function - you do not need to specify any routes here, use abort and make response because this helper function isnt using certain things to create json
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))


    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book {book_id} not found"}, 404))
    return book

    
        
#route functions
@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    books_response = []

    title_query = request.args.get("title")
    
    if title_query is not None:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

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
        "description": book.description,
    }


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()
    try:
        book.title = request_body["title"]
        book.description = request_body["description"]
    except KeyError:
        return {
            "msg": "title and description are required"}, 400
        

    db.session.commit() 
    #always use commit() so that it actually makes the change
    return make_response(f"Book #{book_id} successfully updated")


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()
    return make_response(f"Book #{book_id} successfully deleted", 200)


#put is changing the entire record whereas a patch is only updating one part, patch can just assign one attribute like only title or only description