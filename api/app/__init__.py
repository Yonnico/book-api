from flask import Flask, jsonify, make_response, request, abort
from flask_httpauth import HTTPBasicAuth

from api.book.services import add_author_to_book, find_book_by_id
from api.book.services import get_all_books, get_all_books_with_authors
from api.book.services import validate_add_book, remove_book

from api.author.services import add_books_to_author, find_author_by_id
from api.author.services import get_all_authors, get_all_authors_with_books
from api.author.services import validate_add_author, remove_books_with_author
from api.author.services import validate_author_id

from api.core.services import validate_len, validate_for_str


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
    with_authors = request.args.get('with-authors')
    books = get_all_books()
    if with_authors or with_authors == '':
        books = get_all_books_with_authors()
    return jsonify({'all_books': books})


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id)
    validate_len(book)
    book = book[0]
    with_authors = request.args.get('with-authors')
    if with_authors or with_authors == '':
        book = add_author_to_book(book)
    return jsonify(book)


@app.route('/book/api/v1.0/books', methods=['POST'])
@auth.login_required
def add_book():
    book = validate_add_book(request.json['title'], request.json['annotation'], request.json['author_id'])
    return jsonify(book)


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def change_book(book_id):
    book = find_book_by_id(book_id)
    validate_len(book)
    book = book[0]
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if not validate_for_str(request.json['title']):
            abort(400)
    if 'annotation' in request.json:
        if not validate_for_str(request.json['annotation']):
            abort(400)
    if 'author_id' in request.json:
        if not validate_author_id(request.json['author_id']):
            abort(400)
    book['title'] = request.json.get('title', book['title'])
    book['annotation'] = request.json.get('annotation', book['annotation'])
    book['author_id'] = request.json.get('author_id', book['author_id'])
    return jsonify(book)


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = find_book_by_id(book_id)
    validate_len(book)
    book = book[0]
    remove_book(book)
    return jsonify({'result': True})


@app.route('/book/api/v1.0/authors', methods=['GET'])
def get_authors():
    with_books = request.args.get('with-books')
    authors = get_all_authors()
    if with_books or with_books == '':
        authors = get_all_authors_with_books()
    return jsonify({'all_authors': authors})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = find_author_by_id(author_id)
    validate_len(author)
    author = author[0]
    with_books = request.args.get('with-books')
    if with_books or with_books == '':
        author = add_books_to_author(author)
    return jsonify(author)


@app.route('/book/api/v1.0/authors', methods=['POST'])
@auth.login_required
def add_author():
    author = validate_add_author(request.json['nickname'], request.json['name'])
    return jsonify(author)


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['PUT'])
@auth.login_required
def change_author(author_id):
    author = find_author_by_id(author_id)
    validate_len(author)
    author = author[0]
    if not request.json:
        abort(400)
    if 'nickname' in request.json:
        if not validate_for_str(request.json['nickname']):
            abort(400)
    if 'name' in request.json:
        if not validate_for_str(request.json['name']):
            abort(400)
    author['nickname'] = request.json.get('nickname', author['nickname'])
    author['name'] = request.json.get('name', author['name'])
    return jsonify(author)


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['DELETE'])
@auth.login_required
def delete_author(author_id):
    author = find_author_by_id(author_id)
    author = author[0]
    validate_len(author)
    remove_books_with_author(author)
    return jsonify({"result": True})