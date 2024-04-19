from flask import Flask
from data import db_session
# from data.books import BOOK
from data.books_api import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/main.db")
    app.register_blueprint(API_GET_BOOK_ON_ID)
    app.register_blueprint(API_GET_ALL_BOOKS)
    app.register_blueprint(BOOKS_BLUEPRINT_FILTER)
    '''b = BOOK()
    b.BOOK_NAME = "HUIGMA"
    b.GENRES = "_2_6_7_"
    b.AUTHOR = "BEBRA"
    b.PUBLISHER = "OPIDA"
    b.DESCRIPTION = "PIGHA"
    db_sess = db_session.create_session()
    db_sess.add(b)
    db_sess.commit()'''
    app.run()


if __name__ == '__main__':
    main()