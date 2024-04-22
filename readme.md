# OSOL (Open-Source Online Library)
*OSOL* - проект **открытой** и **удобной** для пользователей любого возраста онлайн библиотеки.
***
### Функционал:
- Скачивание или онлайн чтение книг
- API, позволяющий работать с нашим проектом не только из браузера
- Загрузка новых книг и удаление старых.
- Панель администратора
***
### Техническое задание:
- **Реализация BackEnd составляющий (т.е. сервера)**
  * Работа с базой данных через _SQLAlchemy_;
  * Получение и обработка информации от пользователей;
  * Отправка данных пользователям (HTML, CSS и файлы книг);
  * Ведение статистики: количество скачиваний, запросы и другая информация;
  * Работа с административной панелью (загрузка и обработка книг, статистика и прочее).
- **Реализация таблицы с книгами _main.db/BOOK_**
    * **ID** - номер книги в базе (_INTEGER_);
    * **BOOK_NAME** - название книги (_STRING_);
    * **AUTHOR** - имя автора (_STRING_);
    * **PUBLISHER** - издательство (_STRING_);
    * **DESCRIPTION** - описание (_STRING_);
    * **OUT_COUNTRY** - страна автора/издания (_STRING_);
    * **GENRES** - жанры (_ARRAY OF STRING_);
    * **FILE_NAME** - название файла (_STRING_);
    * **CODECS** - доступные типы файлов (_ARRAY OF STRING_);
    * **CODECS_HASH** - контрольные суммы файлов (_ARRAY OF STRING_);
    * **CREATE_DATE** - дата добавления в базу (_DATE_).
- **Реализация таблицы API-токенов _main.db/API_**
    * **ID** - Уникальный номер токена (_INTEGER_);
    * **TOKEN** - сам ключ-токен (_STRING_);
    * **DEACTIVATE** - рабочий ли ключ? (_BOOLEAN_);
    * **RULE_WORK_WITH_FILTER** - можно ли работать с фильтрами? (_BOOLEAN_);
    * **RULE_GET_ALL_BOOKS** - можно ли получить все книги? (_BOOLEAN_);
    * **RULE_WORK_WITH_BASE** - можно ли работать с базой? (_BOOLEAN_);
    * **RULE_FIND_DATA_BY_STRING** - можно ли работать с базой? (_BOOLEAN_).
- **Реализация UI для работы с пользователем (FrontEnd)**
  * Шапка сайта (_на всех страницах_);
  * "...\" (_главная страница_);
    * Карусель с интересными/популярными книгами;
  * "...\catalog\" (_каталог с книгами_);
    * Фильтры (название, автор, дата выхода);
    * Поиск (по описанию и/или названию);
    * Предложенные варианты (книги);
  * "...\book\{ID}" (_Страница книги_);
    * Вся полученная информация из базы;
    * Кнопки для скачивания;
  * Подвал (то есть низ с контактной информацией) (_на всех страницах_).
- **Создание API**
  * "...\api\all\" (_Получение всех книг из базы_);
    * **?token={user_token}** - токен, имеющий возможность выполнения операции.
  * "...\api\find\" (_Поиск книги в базе по строке_)
    * **?find={user_string}** - строка для поиска;
    * **?name={boolean}** - выполнять поиск в названии;
    * **?description={boolean}** - выполнять поиск по описанию;
    * **?author={boolean}** - выполнять поиск по имени автора;
    * **?publisher={boolean}** - выполнять поиск по издательству;
    * **?genres={genres_id}** - жанр по ID;
    * **?codecs={codecs_id}** - поиск по доступным типам файлов;
    * **?country={country_id}** - поиск по стране выхода.
    * **?token={user_token}** - токен, имеющий возможность выполнения операции.