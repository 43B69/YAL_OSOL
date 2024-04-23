from flask import Flask
from data import db_session
from data.books_api import *
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/books/all", methods=["GET"])
def GET_ALL_BOOKS():
    return jsonify(requests.get("http://127.0.0.1:5000/api/books/all").json())


@app.route("/books/<int: id>", methods=["GET"])
def GET_BOOKS_ID(id):
    return jsonify(requests.get(f"http://127.0.0.1:5000/api/books/{id}").json())


def main():
    db_session.global_init("db/main.db")
    app.register_blueprint(API_GET_BOOK_ON_ID)
    app.register_blueprint(API_GET_ALL_BOOKS)
    app.register_blueprint(BOOKS_BLUEPRINT_FILTER)
    app.register_blueprint(BOOKS_BLUEPRINT_ADD)
    app.run()


if __name__ == '__main__':
    main()
