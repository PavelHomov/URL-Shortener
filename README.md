# Проект URL-Shortener
![Презентация](./media_for_readme/Presentation.gif)
## Примеры запросов к API описаны в файле спецификации `openapi.yml`.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:PavelHomov/URL-Shortener.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Создать файл .env с переменными окружения. Пример наполнения:
```
FLASK_APP=url_shortener
FLASK_ENV=development
SECRET_KEY= MY_SECRET_KEY
DATABASE_URI=sqlite:///db.sqlite3
```
Создать базу данных:
```
flask db upgrade
Либо вручную через оболочку Flask
```
Запустить сервис на локальном сервере:
```
flask run
```
