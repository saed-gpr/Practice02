from fastapi import FastAPI, Query, HTTPException, status, Path
from fastapi.responses import JSONResponse
from typing import Optional
from random import randint

app = FastAPI()

# for test
costs_db = [
    {
        'id' : 1,
        'description' : 'a simple text',
        'amount' : 4

    }
]

# Create
@app.post('/newcost')
def new_cost(description : str, amount : float):

    new = {
        'id' : randint(2, 100),
        'description' : description,
        'amount' : amount
    }

    costs_db.append(new)
    return JSONResponse(content= new, status_code=status.HTTP_200_OK)

# Read
@app.get('/costslist')
def show_all():
    return costs_db

# Search
@app.get('/cost/{cost_id}')
def search_cost(cost_id: int = Path(..., description='enter the custid')):
    if cost_id:
        result = [information for information in costs_db if cost_id == information['id']]
        if len(result) >= 1:
            return JSONResponse(content= result, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f'there is no cost like {cost_id}')

# update
@app.put('/edit/{item_id}')
def update_cost(item_id : int, description : str, cost : float):
    for item in costs_db:
        if item['id'] == item_id:
            item['description'] = description
            item['amount'] = cost

            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

# Delete
@app.delete('/delete/{item_id}')
def delete_cost(item_id : int):
    for item in costs_db:
        if item['id'] == item_id:
            costs_db.remove(item)
            return {'message' : 'cost deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)