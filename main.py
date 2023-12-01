from fastapi import FastAPI, HTTPException, status

app = FastAPI()
items = []
items_id = 1


@app.get('/')
def root():
    return {'message': 'Hello World'}


@app.get('/items')
def get_item(item_id: int):
    try:
        return items[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='item does not exists')


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='item does not exists')


@app.put('/items')
def patch_item(item_id: int, new_name: str, new_coast: float, new_in_stock: bool):
    try:
        items[item_id - 1]['name'] = new_name
        items[item_id - 1]['coast'] = new_coast
        items[item_id - 1]['in_stock'] = new_in_stock
        return items[item_id - 1]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='item does not exists')


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='item does not exists')
