import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


# Объект класса - книга. Каждый аргумент расписан отдельно внутри класса.
class BOOK(SqlAlchemyBase):
    __tablename__ = 'BOOK'

    # Уникальный номер книги. Создаётся автоматически. Неизменяем.
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    # Название книги. Основное название используемое в публицистике.
    BOOK_NAME = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Альтернативные названия книги. Здесь может быть всё что угодно. Не обязательный параметр.
    BOOK_ALTER_NAME = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # ФИО/псевдоним автора. В случае народа: "Устное народное творчество {НАЗВАНИЕ СТРАНЫ}".
    AUTHOR = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Издательство. Если нет - пропускаем. База самостоятельно заменит на "Неизвестно" / "Авторская версия".
    PUBLISHER = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Описание. Кратко, просто и лаконично завлекаем читателя.
    DESCRIPTION = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Дата выхода. Если нет - пропускаем. База самостоятельно заменит на "Неизвестно".
    OUT_DATE = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Страна выпуска. В теории должно быть, но если нет - пропускаем. Базой меняется на "Мир".
    OUT_COUNTRY = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Жанры. Хотя бы один жанр нужно добавить. Количество не ограничено.
    GENRES = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Имя файла. Одинаково для всех типов. Уникально. Записывает транслитом "{BOOK_NAME}-{AUTHOR}-{HASH[:10]}".
    FILE_NAME = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    # Типы файлов. Минимально один. Желательно, чтобы был хотя бы "*.PDF" или "*.TXT".
    CODECS = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Контрольные суммы файлов. Проверяются только при старте сервера.
    CODECS_HASH = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # Количество скачиваний. Общая сумма для всех типов файлов.
    DOWNLOADS = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # Дата загрузки на сервер. На случай фильтра по дате обновления
    CREATE_DATE = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # Рейтинг. Ставится по мнению админа.
    # SCORE = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
