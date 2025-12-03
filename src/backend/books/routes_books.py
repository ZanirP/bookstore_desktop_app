from flask import Blueprint, request, jsonify, abort
from backend.database.models import Book, Genre, book_genres, Review
from backend.database import db
from backend.utils import require_account, require_manager
from datetime import datetime

books_bp = Blueprint("books", __name__)

@books_bp.get("/")
def list_books():
    title = request.args.get("title")
    author = request.args.get("author")
    genre = request.args.get("genre")

    query = Book.query

    if title:
        query = query.filter(Book.title.ilike(f"%{q}%"))

    if author:
        query = query.filter(Book.author.ilike(f"%{q}%"))

    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    books = query.all()
    result = []
    for book in books:
        result.append({
            "id": book.book_id,
            "title": book.title,
            "author": book.author,
            "price_buy": book.price_buy,
            "price_rent": book.price_rent,
            "synopsis": book.synopsis,
        })
    return jsonify(result)

@books_bp.get("/<int:id>")
def get_book_information(id):
    book = Book.query.filter_by(book_id=id).first()
    if not book:
        abort(404)
    result = {
        "id": book.book_id,
        "title": book.title,
        "author": book.author,
        "price_buy": book.price_buy,
        "price_rent": book.price_rent,
        "synopsis": book.synopsis,
    }
    return jsonify(result)

@books_bp.get("/search")
def search_books():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    q = f"%{query}%"
    title_matches = Book.query.filter(Book.title.ilike(q)).all()

    author_matches = (
        Book.query.filter(Book.author.ilike(q))
        .filter(~Book.book_id.in_([b.book_id for b in title_matches]))
        .all()
    )
    genre_rows = Genre.query.filter(Genre.name.ilike(q)).all()
    genre_ids = [g.genre_id for g in genre_rows]

    if genre_ids:
        genre_matches = (
            Book.query.join(Book.genres)
            .filter(Genre.genre_id.in_(genre_ids))
            .filter(~Book.book_id.in_([b.book_id for b in title_matches]))
            .filter(~Book.book_id.in_([b.book_id for b in author_matches]))
            .all()
        )
    else:
        genre_matches = []

    results = title_matches + author_matches + genre_matches

    output = []
    for b in results:
        output.append({
            "id": b.book_id,
            "title": b.title,
            "author": b.author,
            "price_buy": b.price_buy,
            "price_rent": b.price_rent,
            "synopsis": b.synopsis,
        })

    return jsonify(output)


@books_bp.get("/genres")
def list_genres():
    genres = Genre.query.all()
    result = []
    for genre in genres:
        result.append({
            "id": genre.genre_id,
            "name": genre.name,
        })
    return jsonify(result)

@books_bp.get("/<int:id>/reviews")
def list_reviews(id):
    reviews = Review.query.filter_by(book_id=id).all()
    result = []
    for review in reviews:
        result.append({
            "book_id": review.book_id,
            "account_id": review.account_id,
            "id": review.review_id,
            "content": review.review_content,
            "time": review.created_at.isoformat(),

        })

    return jsonify(result)


@books_bp.post("/<int:id>/reviews")
def create_reviews(id):
    account, err, code = require_account(id)
    if err:
        return err, code

    data = request.json
    content = data.get("content")

    if not content:
        return {"error": "Missing content"}, 400

    book = Book.query.get(id)
    if not book:
        return {"error": "Book not found"}, 404

    review = Review(
        book_id=book.book_id,
        account_id=account.account_id,
        review_content=content,
        created_at=datetime.now(),
    )

    db.session.add(review)
    db.session.commit()

    return {"message": "Review added successfully"}, 201

@books_bp.post("/")
def add_book():
    account, err, code = require_manager()
    if err:
        return err, code

    data = request.json
    if not data:
        return {"error": "Missing data"}, 400

    book = Book(
        title=data.get("title"),
        author=data.get("author"),
        synopsis=data.get("synopsis"),
        price_buy=data.get("price_buy"),
        price_rent=data.get("price_rent"),
        created_at=datetime.now(),
    )

    db.session.add(book)
    db.session.commit()

    return {"message": "Book added successfully", "book_id": book.book_id}, 201


@books_bp.patch("/<int:book_id>")
def update_book(book_id):
    account, err, code = require_manager()
    if err:
        return err, code

    book = Book.query.get(book_id)
    if not book:
        return {"error": "Book not found"}, 404

    data = request.json or {}

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.synopsis = data.get("synopsis", book.synopsis)
    book.price_buy = data.get("price_buy", book.price_buy)
    book.price_rent = data.get("price_rent", book.price_rent)

    db.session.commit()

    return {"message": "Book updated"}

