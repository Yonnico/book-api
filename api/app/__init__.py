from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

from api.author.db import all_authors
from api.book.db import all_books

from api.author.services import add_books_to_author, find_author_by_id, is_author_id_exist
from api.book.services import add_author_to_book, find_book_by_id


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
    books = all_books
    if with_authors or with_authors == '':
        books = list(map(add_author_to_book, all_books))
    return jsonify({'all_books': books})


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id)
    book = book[0]
    if not len(book):
        abort(404)
    with_authors = request.args.get('with-authors')
    if with_authors or with_authors == '':
        book = add_author_to_book(book)
    return jsonify({'book': book})


@app.route('/book/api/v1.0/books', methods=['POST'])
@auth.login_required
def add_book():
    if not request.json:
        abort(400)
    if not 'title' in request.json:
        abort(400)
    if not 'annotation' in request.json:
        abort(400)
    if not 'author_id' in request.json:
        abort(400)
    if 'title' in request.json:
        if not isinstance(request.json['title'], str) or not len(request.json['title']):
            abort(400)
    if 'annotation' in request.json:
        if not isinstance(request.json['annotation'], str) or not len(request.json['annotation']):
            abort(400)
    if 'author_id' in request.json:
        if not isinstance(request.json['author_id'], int) or not is_author_id_exist(request.json['author_id']):
            abort(400)

    book = {
        'id': all_books[-1]['id'] + 1,
        'title': request.json['title'],
        'annotation': request.json['annotation'],
        'author_id': request.json['author_id']
    }
    all_books.append(book)
    return jsonify({'book': book}), 201


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def change_book(book_id):
    book = find_book_by_id(book_id)
    if not len(book):
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if not isinstance(request.json['title'], str) or not len(request.json['title']):
            abort(400)
    if 'annotation' in request.json:
        if not isinstance(request.json['annotation'], str) or not len(request.json['annotation']):
            abort(400)
    if 'author_id' in request.json:
        if not isinstance(request.json['author_id'], int) or not is_author_id_exist(request.json['author_id']):
            abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['annotation'] = request.json.get('annotation', book[0]['annotation'])
    book[0]['author_id'] = request.json.get('author_id', book[0]['author_id'])
    return jsonify({'book': book[0]})


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = find_book_by_id(book_id)
    if not len(book):
        abort(404)
    all_books.remove(book[0])
    return jsonify({'result': True})


@app.route('/book/api/v1.0/authors', methods=['GET'])
def get_authors():
    with_books = request.args.get('with-books')
    authors = all_authors
    if with_books or with_books == '':
        authors = list(map(add_books_to_author, all_authors))
    return jsonify({'all_authors': authors})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = find_author_by_id(author_id)
    author = author[0]
    if not len(author):
        abort(404)
    with_books = request.args.get('with-books')
    if with_books or with_books == '':
        author = add_books_to_author(author)
    return jsonify({'author': author})


@app.route('/book/api/v1.0/authors', methods=['POST'])
@auth.login_required
def add_author():
    if not request.json:
        abort(400)
    if 'nickname' not in request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'nickname' in request.json:
        if not isinstance(request.json['nickname'], str) or not len(request.json['nickname']):
            abort(400)
    if 'name' in request.json:
        if not isinstance(request.json['name'], str) or not len(request.json['name']):
            abort(400)

    author = {
        'id': all_authors[-1]['id'] + 1,
        'nickname': request.json['nickname'],
        'name': request.json['name']
    }
    all_authors.append(author)
    return jsonify({'author': author}), 201


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['PUT'])
@auth.login_required
def change_author(author_id):
    author = find_author_by_id(author_id)
    if not len(author):
        abort(404)
    if not request.json:
        abort(400)
    if 'nickname' in request.json:
        if not isinstance(request.json['nickname'], str) or not len(request.json['nickname']):
            abort(400)
    if 'name' in request.json:
        if not isinstance(request.json['name'], str) or not len(request.json['name']):
            abort(400)
    author[0]['nickname'] = request.json.get('nickname', author[0]['nickname'])
    author[0]['name'] = request.json.get('name', author[0]['name'])
    return jsonify({'author': author[0]})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['DELETE'])
@auth.login_required
def delete_author(author_id):
    author = find_author_by_id(author_id)
    if not len(author):
        abort(404)
    all_authors.remove(author[0])
    return jsonify({'result': True})