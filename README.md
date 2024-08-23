### Online Store

Проект **Online Store** представляет собой интернет-магазин, реализованный на DRF. Включает в себя функционал управления категориями, продуктами, корзиной и пользователями.

### Автор:

Автор: Nikita Blokhin
GitHub: github.com/bignikkk

### Технологии:

Python
DRF
SQLite3

### Как развернуть проект локально:

```
git clone https://github.com/bignikkk/the_online_store
```

Перейти в деректорию online_store:

```
cd online_store
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Провести миграции командой:

```
python manage.py migrate
```

Запустить сервер командой:

```
python manage.py runserver
```

