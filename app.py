from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)


def add_author_to_book(book):
    author = list(filter(lambda author: author['id'] == 
    book['author_id'], all_authors))
    author = author[0]
    book_with_author = book.copy()
    book_with_author.pop('author_id')
    book_with_author['author'] = author
    return book_with_author


def add_books_to_author(author):
    books = list(filter(lambda book: book['author_id'] == 
    author['id'], all_books))
    author_with_books = author.copy()
    author_with_books['books'] = books
    return author_with_books


def find_book_by_id(book_id):
    book = list(filter(lambda b: b['id'] == book_id, all_books))
    return book


def find_author_by_id(author_id):
    author = list(filter(lambda a: a['id'] == author_id, all_authors))
    return author


def is_author_id_exist(id):
    value = False
    for author in all_authors:
        if author['id'] == id:
            value = True
    return value


all_books = [
    {
        'id': 1,
        'title': 'Война и мир',
        'annotation': 'Про книгу война и мир',
        'author_id': 1
    },
    {
        'id': 2,
        'title': 'Евгений Онегин',
        'annotation': 'Про книгу Евгений Онегин',
        'author_id': 2
    },
    {
        'id': 3,
        'title': 'Анна Каренина',
        'annotation': 'Про книгу Анна Каренина',
        'author_id': 1
    },
    {
        'id': 4,
        'title': 'Полтава',
        'annotation': 'Про книгу Полтава',
        'author_id': 2
    }
]


all_authors = [
    {
        'id': 1,
        'nickname': 'TolstoyProd',
        'name': 'Лев Толстой'
    },
    {
        'id': 2,
        'nickname': 'PushkinProd',
        'name': 'Александр Пушкин'
    }
]


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
    return jsonify({'all_books': all_books})


@app.route('/book/api/v1.0/books_with_author', methods=['GET'])
def get_books_with_author():
    return jsonify({'books_with_author': list(map(add_author_to_book, all_books))})


@app.route('/book/api/v1.0/authors', methods=['GET'])
def get_authors():
    return jsonify({'all_authors': all_authors})

@app.route('/book/api/v1.0/authors_with_books', methods=['GET'])
def get_authors_with_books():
    return jsonify({'authors_with_books': list(map(add_books_to_author, all_authors))})


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = find_book_by_id(book_id)
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})


@app.route('/book/api/v1.0/books_with_author/<int:book_id>', methods=['GET'])
def get_book_with_author(book_id):
    book = find_book_by_id(book_id)
    if len(book) == 0:
        abort(404)
    return jsonify({'book_with_author': add_author_to_book(book[0])})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = find_author_by_id(author_id)
    if len(author) == 0:
        abort(404)
    return jsonify({'author': author[0]})


@app.route('/book/api/v1.0/authors_with_books/<int:author_id>', methods=['GET'])
def get_author_with_books(author_id):
    author = find_author_by_id(author_id)
    if len(author) == 0:
        abort(404)
    return jsonify({'author_with_books': add_books_to_author(author[0])})


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


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def change_book(book_id):
    book = find_book_by_id(book_id)
    if len(book) == 0:
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
        if not isinstance(request.json['author_id'], int) or request.json['author_id'] > len(all_authors):
            abort(400)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['annotation'] = request.json.get('annotation', book[0]['annotation'])
    book[0]['author_id'] = request.json.get('author_id', book[0]['author_id'])
    return jsonify({'book': book[0]})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['PUT'])
@auth.login_required
def change_author(author_id):
    author = find_author_by_id(author_id)
    if len(author) == 0:
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


@app.route('/book/api/v1.0/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = find_book_by_id(book_id)
    if len(book) == 0:
        abort(404)
    all_books.remove(book[0])
    return jsonify({'result': True})


@app.route('/book/api/v1.0/authors/<int:author_id>', methods=['DELETE'])
@auth.login_required
def delete_author(author_id):
    author = find_author_by_id(author_id)
    if len(author) == 0:
        abort(404)
    all_authors.remove(author[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)