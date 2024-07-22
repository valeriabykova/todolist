from fastapi import Depends, FastAPI, Request, status, HTTPException
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from fastapi.responses import HTMLResponse
import app.models as models, app.schemas as schemas
from app.database import Base
from sqlalchemy import desc, or_
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="app/templates")


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/tasks")
def homepage(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

@app.get("/tasks/by/{column}")
def sorted_by(column : schemas.SortEnum, db: Session = Depends(get_db), reverse : bool = True):
    if reverse:
        tasks = db.query(models.Task).order_by(column).all()
    else:
        tasks = db.query(models.Task).order_by(desc(column)).all()
    return tasks

@app.get("/tasks/by/top/{n}")
def get_first_n(n: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by("priority").limit(n).all()
    return tasks

@app.post("/tasks")
def add(task : schemas.CreateTask, db: Session = Depends(get_db)):
    print(task)
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id:  int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=400, detail="Bad request")
    return task

@app.get("/tasks/search/{substring}")
def get_task_by_substr(substring: str, db: Session = Depends(get_db)):
    task =  db.query(models.Task).filter(or_(models.Task.name.contains(substring), models.Task.description.contains(substring))).all()
    if task is None:
        return {"status": status.HTTP_400_BAD_REQUEST, "error": "tasks not found"} 
    return task

@app.put("/tasks/{task_id}/update_status")
def update_status(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return {"status": status.HTTP_400_BAD_REQUEST, "error": "task not found"} 
    task.status = (task.status) % 4 + 1
    db.commit()
    return {"status": status.HTTP_200_OK}

@app.put("/tasks/{task_id}/update_priority")
def update_priority(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        return {"status": status.HTTP_400_BAD_REQUEST, "error": "task not found"} 
    task.priority = (task.priority) % 5 + 1
    db.commit()
    return {"status": status.HTTP_200_OK}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).delete()
    if task is None:
        return {"status": status.HTTP_400_BAD_REQUEST, "error": "task not found"} 
    db.commit()
    return {"status": status.HTTP_200_OK}
    

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)