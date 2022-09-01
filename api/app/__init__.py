from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth

from api.book.services import get_author_to_book, get_book_by_id, validate_and_change_book
from api.book.services import get_all_books, get_all_books_with_authors
from api.book.services import validate_and_add_book, remove_book

from api.author.services import get_books_to_author, get_author_by_id, validate_and_change_author
from api.author.services import get_all_authors, get_all_authors_with_books
from api.author.services import validate_and_add_author, remove_books_with_author


app = Flask(__name__)


auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'Morzh':
        return 'Walrus'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized  acess'}), 401)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/book/api/v1.0/books', methods=['GET'])
def get_books():
    books = get_all_books()
    with_authors = request.args.get('with-authors')
    if with_authors or with_authors == '':
        books = get_all_books_with_authors()
    return jsonify({'all_books': books})


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        abort(404)
    with_authors = request.args.get('with-authors')
    if with_authors or with_authors == '':
        book = get_author_to_book(book)
    return jsonify(book)


@app.route('/book/api/v1.0/books', methods=['POST'])
@auth.login_required
def add_book():
    book = validate_and_add_book(
        request.json['title'],
        request.json['annotation'],
        request.json['author_id']
    )
    if not book:
        abort(400)
    return jsonify(book)


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def change_book(book_id):
    response = validate_and_change_book(
        book_id,
        request.json.get('title', None),
        request.json.get('annotation', None),
        request.json.get('author_id', None)
    )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    return jsonify(response['value'])


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        abort(404)
    remove_book(book)
    return jsonify({'result': True})


@app.route('/book/api/v1.0/authors', methods=['GET'])
def get_authors():
    authors = get_all_authors()
    with_books = request.args.get('with-books')
    if with_books or with_books == '':
        authors = get_all_authors_with_books()
    return jsonify({'all_authors': authors})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = get_author_by_id(author_id)
    if not author:
        abort(404)
    with_books = request.args.get('with-books')
    if with_books or with_books == '':
        author = get_books_to_author(author)
    return jsonify(author)


@app.route('/book/api/v1.0/authors', methods=['POST'])
@auth.login_required
def add_author():
    author = validate_and_add_author(
        request.json['nickname'],
        request.json['name']
    )
    if not author:
        abort(400)
    return jsonify(author)


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['PUT'])
@auth.login_required
def change_author(author_id):
    response = validate_and_change_author(
        author_id,
        request.json.get('nickname', None),
        request.json.get('name', None)
        )
    if response['status'] == 0:
        abort(404)
    if response['status'] == 1:
        abort(400)
    return jsonify(response['value'])


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['DELETE'])
@auth.login_required
def delete_author(author_id):
    author = get_author_by_id(author_id)
    if not author:
        abort(404)
    remove_books_with_author(author)
    return jsonify({"result": True})