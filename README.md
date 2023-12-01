# Создание и контейниризация простого веб-приложения на FastAPI

## Настройка виртуального окружения и зависимостей

Для выполнения данного задания Вам понадобится python и docker. Установите их перед началом выполнения.

1. Склонируйте данный репозиторий

2. Перейдите в него

3. Создайте виртуальное окружение

```
python3 -m venv venv
```

4. Активируйте его

```
source venv/bin/activate
```

Для установки зависимостей мы будем использовать библиотеку pip-tools, так как она автоматически определяет совместимые версии для разных библиотек и фреймворков

5. Установите pip-tools

```
pip install pip-tools
```

6. Создайте файл requirements.in и откройте его

7. Запишите в данный файл следующие строки

```
fastapi
uvicorn
```

8. Далее в консоли с активированным виртуальным окружением пишем

```
pip-compile
```

У нас автоматически создаться requirements.txt, в котором будут библиотеки и фреймворки совместимых версий

```
pip-sync
```

Далее данной командой все библиотеки установятся в наше виртуальное окружение

Теперь мы готовы писать само приложение

# Написание веб-приложения

Мы разработаем простое веб-приложение, которое будет работать с абстрактными элементами (назовем их items). Наше приложение сможет хранить items, также по запросу пользователя приложение сможет добавлять новые items, изменять их и удалять. В item будут лежать данные о его названии, цене и наличии.

1. Создать файл main.py и запустить его

2. Далее импортируем классы FastAPI, HTTPException, status для дальнейшей работы с ними

```
from fastapi import FastAPI, HTTPException, status
```

3. Создаем экземпляр класса FastAPI для создания нашего приложения. Также нам потребуется создать список items для хранения данных и переменную items_id для идентификации items

```
app = FastAPI()
items = []
items_id = 1
```

4. Создадим первый endpoint, который будет возвращать сообщение "Hello World"

```
@app.get('/')
def root():
    return {'message': 'Hello World'}
```

5. Далее создадим endpoint '/items', который будет обрабатывать GET-запросы и возвращать требуемый item, если он существует

```
@app.get('/items')
def get_item(item_id: int):
    try:
        return items[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='item does not exists')
```

Проверка существования item происходит за счёт блока try except. Если элемента с переданным id не существует, будет вызвано исключение IndexError, так как мы выйдем за границы нашего списка. Если элемента не существует, мы оповещаем об этом пользователя статус-кодом 400 и сообщением "item does not exists"

6. Теперь создадим endpoint '/items', который будет обрабатывать POST-запросы, создавать item и добавлять его в список items

```
@app.post('/items')
def create_item(name: str, coast: float, in_stock: bool):
    global items_id
    item = {
        'id': items_id,
        'name': name,
        'coast': coast,
        'in_stock': in_stock
    }
    items.append(item)
    items_id += 1
    return item
```

Мы работаем с глобальной переменной items_id, так как у каждого item должен быть уникальный id, поэтому перед return увеличиваем её на 1

7. По этому же endpoint будем обрабатывать PATCH-запросы для частичного изменения требуемого item

```
@app.patch('/items')
def patch_item(item_id: int, new_name: str = None, new_coast: float = None, new_in_stock: bool = None):
    try:
        if new_name:
            items[item_id - 1]['name'] = new_name
            return items[item_id - 1]
        elif new_coast:
            items[item_id - 1]['coast'] = new_coast
            return items[item_id - 1]
        elif new_in_stock:
            items[item_id - 1]['in_stock'] = new_in_stock
            return items[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='item does not exists')
```

Так же, как и при обработке GET-запросов будем проверять, существует ли требуемый item

8. Теперь будем обрабатывать PUT-запросы для полного изменения требуемого item

```
@app.put('/items')
def patch_item(item_id: int, new_name: str, new_coast: float, new_in_stock: bool):
    try:
        items[item_id - 1]['name'] = new_name
        items[item_id - 1]['coast'] = new_coast
        items[item_id - 1]['in_stock'] = new_in_stock
        return items[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='item does not exists')
```

Все так же, как и в прошлом пункте, только требуемый item изменяется полностью

9. Создадим обработчик DELETE-запросов для удаления требуемого item

```
@app.delete('/items')
def delete_item(item_id: int):
    global items_id
    try:
        if item_id != len(items):
            for index in range(item_id, len(items)):
                items[index]['id'] -= 1
        item = items.pop(item_id - 1)
        items_id -= 1
        return item
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='item does not exists')
```

Наше приложение готово. Теперь можно запустить его и проверить работоспособность.

# Запуск веб-приложения

Теперь мы можем запустить наше веб-приложение, для этого введем команду

```
uvicorn main:app
```

Теперь мы можем перейти по ссылке [localhost:8000/docs](http://localhost:8000/docs) и делать запросы к нашему приложению

# Контейнеризация приложения

1. Создать Dockerfile и запустить его

2. Сначала импортируем образ python

```
FROM python:yourversion
```

Вместо yourversion напишите вашу версию python

3. Теперь сделаем рабочую директорию app

```
WORKDIR /app
```

4. Далее скопируем файлы, необходимые для работы нашего приложения

```
COPY ./main.py /app
COPY ./requirements.txt /app
```

5. Установим зависимости внутри образа

```
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
```

6. Наконец, напишем последнюю команду, которая будет исполняться при запуске контейнера

```
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

Флаг --host 0.0.0.0 отвечает за то, чтобы наше веб-приложение работало на всех сетевых интерфейсах контейнера на порту 80.

7. Теперь создадим образ. Впишем в консоли

```
docker build -t fastapiapp .
```

8. Запустим контейнер, используя образ fastapiapp

```
docker run -d --name fastapiapp -p 8000:80 fastapiapp
```

Флаг -d отвечает за запуск контейнера в фоновом режиме. Флагом --name задаем имя нашему контейнеру. Флагом -p мы пробрасываем 80 порт контейнера на 8000 порт хоста

# Проверка работоспособности

Теперь можем перейти по ссылке [localhost:8000/docs](http://localhost:8000/docs) и проверить работоспособность нашего веб-приложения

Чтобы остановить работу контейнера, надо прописать данную команду в консоль

```
docker stop fastapiapp
```
