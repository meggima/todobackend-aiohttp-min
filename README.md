# todobackend-aiohttp

Yet another [todo backend](http://todobackend.com) written in Python 3.5 with aiohttp. Original code [from alec.thoughts import \*](http://justanr.github.io/getting-start-with-aiohttpweb-a-todo-tutorial).

## Usage

The application uses an Sqlite database. The DB can be initialized using the script `init.sql`.

```
sqlite3 tasks.db -init init.sql
pip3 install -r requirements.txt
python3 aiotodo.py
```

## Tests

You can run validate the application with http://www.todobackend.com/specs/.
