from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from fastapi import FastAPI, Depends, Request, Form, status

from database import SessionLocal, Session
import models

templates = Jinja2Templates(directory="templates")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/")
def home(req: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("base.html", { "request": req, "todo_list": todos })

@app.post("/add")
def add(req: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home") # url = "/"
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/update/{todo_id}")
def update(req: Request, todo_id: int, title: str = Form(...), db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    todo.title = title
    db.commit()
    url = app.url_path_for("home") # url = "/"
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/toggle/{todo_id}")
def toggle(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    todo.complete = not todo.complete
    db.commit()
    url = app.url_path_for("home") # url = "/"
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{todo_id}")
def delete(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home") # url = "/"
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, port=8000)