from flask import Flask
from data import db_session
# from data.books import BOOK
from data.books_api import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/books.db")
    app.register_blueprint(BOOKS_BLUEPRINT_GET_USING_ID)
    app.register_blueprint(BOOKS_BLUEPRINT_GET_ALL)
    app.run()


if __name__ == '__main__':
    main()