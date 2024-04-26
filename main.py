from flask import Flask, render_template
from data import db_session
from data.books_api import *
import requests
import jinja2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
f = open("db/genres.csv", "r", encoding="UTF-8")
genres = {int(i.split(";")[0]): i.split(";")[1] for i in f.readlines()}
f.close()
f = open("bootstrap.min.css", "r", encoding="UTF-8")
BOOTSTRAP = "".join([i for i in f.readlines()])
f.close()
environment = jinja2.Environment()


@app.route("/filter", methods=["GET"])
def FILTRATION():
    args = request.args.to_dict()
    string = "https:/127.0.0.1:5000/api/filter?"
    for i in args.keys():
        string += f"{i}={args[i]}&"
    return requests.get(string[:-1])


@app.route("/books/all", methods=["GET"])
def GET_ALL_BOOKS():
    data = jsonify(requests.get("http://127.0.0.1:5000/api/books/all").json())
    return data

@app.route("/books/bootstrap.min.css", methods=["GET"])
def RETURN_BOOTSTRAP():
    return BOOTSTRAP


@app.route("/books/<int:id>", methods=["GET"])
def GET_BOOKS_ID(id):
    data = requests.get(f"http://127.0.0.1:5000/api/books/{id}").json()
    print(data)
    param = {}
    param["title"] = data[0]
    param["book_name"] = data[0]
    param["author"] = data[1]
    param["genres"] = ", ".join([genres[i] for i in data[5]])
    param["static_img"] = "static/img.png"
    xl = open("templates/book.html", "r")
    template = environment.from_string("".join(xl.readlines()))
    xl.close()
    # make_response("img.png")
    return render_template("book.html", **param)


def main():
    db_session.global_init("db/main.db")
    app.register_blueprint(API_GET_BOOK_ON_ID)
    app.register_blueprint(API_GET_ALL_BOOKS)
    app.register_blueprint(BOOKS_BLUEPRINT_FILTER)
    app.register_blueprint(BOOKS_BLUEPRINT_ADD)
    app.run()


if __name__ == '__main__':
    main()
