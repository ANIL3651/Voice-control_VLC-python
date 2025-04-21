from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Todo List API")


# Pydantic model for Todo
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Todo(TodoCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# In-memory storage for todos (in a real app, you'd use a database)
todos = []
todo_id_counter = 1


@app.post("/todos/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate):
    global todo_id_counter
    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.now()
    )
    todos.append(new_todo)
    todo_id_counter += 1
    return new_todo


@app.get("/todos/", response_model=List[Todo])
def get_todos():
    return todos


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = next((todo for todo in todos if todo.id == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate):
    todo_idx = next((idx for idx, todo in enumerate(todos) if todo.id == todo_id), None)
    if todo_idx is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    current_todo = todos[todo_idx]
    updated_todo_dict = updated_todo.dict()

    todos[todo_idx] = Todo(
        id=current_todo.id,
        created_at=current_todo.created_at,
        **updated_todo_dict
    )
    return todos[todo_idx]


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    todo_idx = next((idx for idx, todo in enumerate(todos) if todo.id == todo_id), None)
    if todo_idx is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(todo_idx)
    return None