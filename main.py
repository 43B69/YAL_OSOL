from flask import Flask, render_template
from data import db_session
from data.books_api import *
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
f = open("db/genres.csv", "r", encoding="UTF-8")
genres = {int(i.split(";")[0]): i.split(";")[1] for i in f.readlines()}
f.close()

'''@app.route("/books/filter", methods=["GET"])
def FILTER_BOOKS():
    '''

@app.route("/books/all", methods=["GET"])
def GET_ALL_BOOKS():
    data = jsonify(requests.get("http://127.0.0.1:5000/api/books/all").json())
    return data


@app.route("/books/<int:id>", methods=["GET"])
def GET_BOOKS_ID(id):
    data = jsonify(requests.get(f"http://127.0.0.1:5000/api/books/{id}").json())
    param = {}
    param["title"] = data[0]
    param["book_name"] = data[0]
    param["author"] = data[1]
    param["genres"] = [genres[i] for i in data[5]]
    return render_template("test/test/book.html", **param)


def main():
    db_session.global_init("db/main.db")
    app.register_blueprint(API_GET_BOOK_ON_ID)
    app.register_blueprint(API_GET_ALL_BOOKS)
    app.register_blueprint(BOOKS_BLUEPRINT_FILTER)
    app.register_blueprint(BOOKS_BLUEPRINT_ADD)
    app.run()


if __name__ == '__main__':
    main()
