from fastapi import FastAPI, Query, HTTPException, status, Path
from fastapi.responses import JSONResponse
from typing import Optional
from random import randint

app = FastAPI()

# for test
expenses_db = {
    1: {
        'id' : 1,
        'description' : 'a simple text',
        'amount' : 4

    }
}

# Create
@app.post('/expenses')
def new_cost(description : str, amount : float):

    new_id = max(expenses_db.keys()) + 1

    new_expense = {
        'id' : new_id,
        'description' : description,
        'amount' : amount
    }

    expenses_db[new_id] = new_expense

    return JSONResponse(
        content=new_expense,
        status_code=status.HTTP_201_CREATED
    )

# Read
@app.get('/expenses')
def get_expenses(description: Optional[str] = None):

    if description:
        result = [
            cost for cost in expenses_db.values()
            if description in cost['description']
        ]

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No expense found"
            )

        return JSONResponse(
            content=result,
            status_code=status.HTTP_200_OK
        )

    return JSONResponse(
        content=list(expenses_db.values()),
        status_code=status.HTTP_200_OK
    )

# Read one expense
@app.get('/expenses/{expense_id}')
def get_expense(expense_id: int):

    if expense_id in expenses_db:
        return JSONResponse(
            content=expenses_db[expense_id],
            status_code=status.HTTP_200_OK
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Expense with id {expense_id} not found"
    )


# Update
@app.put('/expenses/{expense_id}')
def update_expense(expense_id: int, description: str, amount: float):

    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )

    expenses_db[expense_id]['description'] = description
    expenses_db[expense_id]['amount'] = amount

    return JSONResponse(
        content=expenses_db[expense_id],
        status_code=status.HTTP_200_OK
    )

# Delete
@app.delete('/expenses/{expense_id}')
def delete_expense(expense_id: int):

    if expense_id not in expenses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found"
        )

    deleted_expense = expenses_db.pop(expense_id)

    return JSONResponse(
        content={
            "message": "Expense deleted successfully",
            "expense": deleted_expense
        },
        status_code=status.HTTP_200_OK
    )