# project-finder-backend

## Как начать работать над репозиторием

1. Клонируем репозиторий `git clone git@gitlab.com:project-finder-team/project-finder-backend.git`
2. Создаем отдельную ветку с фичей, над которой будем работать `git checkout -b <branch-name>`
3. Создать файл `.env` и прописать необходимые аргументы

```bash
# .env
HOST=127.0.0.1
PORT=3000
TYPE=DEVELOPMENT
```

4. Создать виртуальное окружение `python3 -m venv env`
5. Активировать виртуально окружение `source env/bin/activate`
6. Установить необходимые зависимости `pip install -r requirements.txt`
7. Запустить сервер `python3 main.py`

### Успех!!!

```shell
$ curl 127.0.0.1:3000/test
{"ok":"works"}
```
