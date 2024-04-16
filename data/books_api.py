import flask
from flask import jsonify, make_response, request
from . import db_session
from .books import BOOK

BOOKS_BLUEPRINT_GET_USING_ID = flask.Blueprint("BOOK_api_ID", __name__)
BOOKS_BLUEPRINT_GET_ALL = flask.Blueprint("BOOK_api_ALL", __name__)
BOOKS_BLUEPRINT_FILTER = flask.Blueprint("BOOK_api_filter", __name__)


@BOOKS_BLUEPRINT_GET_USING_ID.route("/api/books/<int:book_id>", methods=["GET"])
def BOOK_api_ID(book_id):
    db_sess = db_session.create_session()
    query_book = db_sess.query(BOOK).filter(BOOK.ID == book_id).first()
    if not query_book:
        return make_response(jsonify({"error": "not found"}), 404)
    return jsonify({query_book.ID: [query_book.BOOK_NAME, query_book.BOOK_ALTER_NAME, query_book.AUTHOR,
                                    query_book.PUBLISHER, query_book.DESCRIPTION, query_book.OUT_DATE,
                                    query_book.OUT_COUNTRY, query_book.GENRES, query_book.FILE_NAME,
                                    query_book.CODECS, query_book.CODECS_HASH, query_book.DOWNLOADS,
                                    query_book.CREATE_DATE]})


@BOOKS_BLUEPRINT_GET_ALL.route("/api/books/all", methods=["GET"])
def BOOK_api_ALL():
    db_sess = db_session.create_session()

    query_all_books = db_sess.query(BOOK).all()
    if not query_all_books:
        return make_response(jsonify({"error": "not found"}), 404)
    res = {}
    for i in query_all_books:
        res[i.ID] = [i.BOOK_NAME, i.BOOK_ALTER_NAME, i.AUTHOR, i.PUBLISHER, i.DESCRIPTION, i.OUT_DATE,
                     i.OUT_COUNTRY, i.GENRES, i.FILE_NAME, i.CODECS, i.CODECS_HASH, i.DOWNLOADS, i.CREATE_DATE]
    return jsonify(res)


@BOOKS_BLUEPRINT_FILTER.route("/api/filter", methods=["GET"])
def BOOK_api_filter():
    args = request.args

    db_sess = db_session.create_session()
    query_all_books = db_sess.query(BOOK).filter()
    return args.to_dict()
