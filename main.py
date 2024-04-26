from flask import Flask, render_template, redirect, send_from_directory, send_file
from data import db_session
from data.books_api import *
import requests
import jinja2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
f = open("db/genres.csv", "r", encoding="UTF-8")
genres = {int(i.split(";")[0]): i.split(";")[1] for i in f.readlines()}
f.close()
f = open("db/codecs.csv", "r", encoding="UTF-8")
codecs = {int(i.split(";")[0]): i.split(";")[1] for i in f.readlines()}
f.close()
f = open("static/bootstrap.min.css", "r", encoding="UTF-8")
BOOTSTRAP = "".join([i for i in f.readlines()])
f.close()
environment = jinja2.Environment()


@app.route("/filter", methods=["GET"])
def FILTRATION():
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


@app.route("/books/all", methods=["GET"])
def GET_ALL_BOOKS():
    data = requests.get("http://127.0.0.1:5000/api/books/all").json()
    return jsonify(data)


@app.route("/books/bootstrap.min.css", methods=["GET"])
def RETURN_BOOTSTRAP():
    return send_from_directory('static', "bootstrap.min.css")


@app.route("/books/static/<data>", methods=["GET"])
def RETURN_PICTURE(data):
    return send_file(data, mimetype='image/gif')


@app.route("/", methods=["GET"])
def HX():
    return redirect("/books/all")


@app.route("/books/<int:id>", methods=["GET"])
def GET_BOOKS_ID(id):
    data = requests.get(f"http://127.0.0.1:5000/api/books/{id}").json()
    print(data)
    param = {}
    param["SUDA_FILE_PON"] = f"/static/{data[6]}.png"
    param["title"] = data[0]
    param["book_name"] = data[0]
    param["author"] = data[1]
    param["genres"] = ", ".join([genres[i] for i in data[5]])
    param["static_img"] = "static/img.png"
    param["AAAAAAA_PUSTITE_MENIA_V_INTERNET"] = f"/static/{data[6]}.pdf"
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
