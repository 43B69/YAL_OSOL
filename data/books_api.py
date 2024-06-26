import flask
from flask import jsonify, make_response, request
from . import db_session
from .books import BOOK

API_GET_BOOK_ON_ID = flask.Blueprint("API_ID", __name__)
API_GET_ALL_BOOKS = flask.Blueprint("API_ALL", __name__)
BOOKS_BLUEPRINT_FILTER = flask.Blueprint("API_FILTER", __name__)
BOOKS_BLUEPRINT_ADD = flask.Blueprint("API_ADD", __name__)
FILTER_NAMES = ["ID", "find", "name", "description", "author", "publisher", "genres", "codecs", "country", "file_name"]
COUNTRIES = {}
with open("db/country.csv", "r", encoding="UTF-8") as f:
    buff = f.readline().split(";")
    COUNTRIES[int(buff[0])] = [buff[1], buff[2]]


def formatter(i):
    res = [i.BOOK_NAME, i.AUTHOR, i.PUBLISHER, i.DESCRIPTION,
           i.OUT_COUNTRY, [int(j) for j in i.GENRES.split(";")[1:-1]], i.FILE_NAME,
           [int(j) for j in i.CODECS.split(";")[1:-1]], i.CODECS_HASH]
    return res


@API_GET_BOOK_ON_ID.route("/api/books/<int:book_id>", methods=["GET"])
def book_api_id(book_id):
    db_sess = db_session.create_session()
    query_book = db_sess.query(BOOK).filter(BOOK.ID == book_id).first()
    if not query_book:
        return make_response(jsonify({"error": "not found"}), 404)
    return formatter(query_book)


@API_GET_ALL_BOOKS.route("/api/books/all", methods=["GET"])
def book_api_all():
    db_sess = db_session.create_session()
    query_all_books = db_sess.query(BOOK).all()
    if not query_all_books:
        return make_response(jsonify({"error": "not found"}), 404)
    res = {}
    for i in query_all_books:
        res[int(i.ID)] = [i.BOOK_NAME, i.AUTHOR, i.PUBLISHER, i.DESCRIPTION,
                          i.OUT_COUNTRY, i.GENRES, i.FILE_NAME, i.CODECS, i.CODECS_HASH, i.CREATE_DATE]
    return jsonify(res)


@BOOKS_BLUEPRINT_ADD.route("/api/add", methods=["POST"])
def book_add():
    args = request.args.to_dict()
    right_args = {i: args[i] for i in args if i in FILTER_NAMES}
    db_sess = db_session.create_session()
    query_all_books = db_sess.query(BOOK)
    input_b = BOOK()
    input_b.BOOK_NAME = right_args["name"]
    input_b.AUTHOR = right_args["author"]
    input_b.DESCRIPTION = right_args["description"]
    input_b.CODECS = right_args["codecs"]
    input_b.OUT_COUNTRY = int(right_args["country"])
    input_b.GENRES = right_args["genres"]
    input_b.FILE_NAME = right_args["file_name"]
    db_sess.add(input_b)
    db_sess.commit()
    return jsonify({int(input_b.ID): [input_b.BOOK_NAME, input_b.AUTHOR,
                                         input_b.PUBLISHER, input_b.DESCRIPTION,
                                         input_b.OUT_COUNTRY, input_b.GENRES, input_b.FILE_NAME,
                                         input_b.CODECS, input_b.CODECS_HASH,
                                         input_b.CREATE_DATE]})


@BOOKS_BLUEPRINT_FILTER.route("/api/filter", methods=["GET"])
def book_api_filter():
    args = request.args.to_dict()
    # Буфер для обработки массивов
    # выписываем только правильные аргументы
    right_args = {i: args[i] for i in args if i in FILTER_NAMES}
    # Начинаем работать с сессией
    db_sess = db_session.create_session()
    query_all_books = db_sess.query(BOOK)
    if "find" in right_args and right_args["find"] != "":
        if "name" in right_args and right_args["name"] == "1":
            query_all_books = query_all_books.filter(BOOK.BOOK_NAME.like(f"%{right_args['find']}%"))
        if "description" in right_args and right_args["description"] == "1":
            query_all_books = query_all_books.filter(BOOK.DESCRIPTION.like(f"%{right_args['find']}%"))
        if "author" in right_args and right_args["author"] == "1":
            query_all_books = query_all_books.filter(BOOK.AUTHOR.like(f"%{right_args['find']}%"))
        if "publisher" in right_args and right_args["publisher"] == "1":
            query_all_books = query_all_books.filter(BOOK.PUBLISHER.like(f"%{right_args['find']}%"))
    if "genres" in right_args and right_args["genres"] != "":
        buff = right_args["genres"].split(";")
        genres = []
        for i in range(len(buff)):
            try:
                int(buff[i])
            except ValueError:
                return make_response(jsonify({"error": "The genre number is a string"}), 400)
            genres.append(int(buff[i]))
        for i in genres:
            query_all_books = query_all_books.filter(BOOK.GENRES.like(f"%;{i};%"))
    if "codecs" in right_args and right_args["codecs"] != "":
        buff = right_args["codecs"].split(";")
        codecs = []
        for i in range(len(buff)):
            try:
                int(buff[i])
            except ValueError:
                return make_response(jsonify({"error": "The genre number is a string"}), 400)
            codecs.append(int(buff[i]))
        for i in codecs:
            query_all_books = query_all_books.filter(BOOK.CODECS.like(f"%;{i};%"))
    if "country" in right_args and right_args["country"] != "":
        query_all_books = query_all_books.filter(BOOK.OUT_COUNTRY.like(int(right_args["country"])))
    data = query_all_books.all()
    res = {}
    for i in data:
        res[int(i.ID)] = [i.BOOK_NAME, i.AUTHOR, i.PUBLISHER, i.DESCRIPTION,
                          i.OUT_COUNTRY, i.GENRES, i.FILE_NAME, i.CODECS, i.CODECS_HASH, i.CREATE_DATE]
    return jsonify(res)
