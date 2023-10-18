from fastapi import FastAPI, Depends, status, HTTPException, Response
from schemas import Blog, UpdateBlog, ShowBlog, User, ShowUser
from typing import List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from hashing import Hash


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

def get_db():
    db = SessionLocal()
    try:
        yield(db)
    finally:
        db.close()
 
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog) 
    return new_blog


@app.get("/blog", tags=["blogs"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", tags=["blogs"])
def get_blog_id(id: int, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put("/blog/{id}", status_code= status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id:int, request: UpdateBlog, db: Session= Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise(HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id of {id} not found"))

    blog.update(request)

    db.commit()
    return "updated"  

@app.post("/user", response_model= ShowUser, tags=["users"])
def create_user(request: User, db: Session= Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model= ShowUser, tags=["users"])
def show_user(id: int, db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@app.get("/users", response_model= List[ShowUser], tags=["users"])
def get_all_usrs(db: Session= Depends(get_db)):
    users = db.query(models.User).all()
    return users

