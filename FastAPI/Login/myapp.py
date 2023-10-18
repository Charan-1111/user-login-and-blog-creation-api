from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schemas import RegisterUser, LoginUser, ShowUser, UserPassword, Blog, ShowBlogs
from hashing import Hash
from pydantic import Field

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

# registration and login section
@app.post("/register", tags=["users"], response_model = ShowUser)
def register_user(request: RegisterUser, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user:
        return f"User with {request.email} already registerd. Please Login"

    else:
        new_user = models.User(name= request.name, email= request.email, password= Hash.bcrypt(request.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

@app.post("/login", tags=["users"])
def user_login(request: UserPassword, db: Session = Depends(get_db)):
    reg_user = db.query(models.User).filter(models.User.email.like(request.email), models.User.password.like(Hash.bcrypt(request.password)))

    if not reg_user:
        return "Your email or password may be wrong. Once check and please try again.!!!!"

    else:
        return "Welcome back {reg_user}."
    

@app.put("/forgot-password", tags=["users"])
def forgot_password(request: UserPassword, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        return "User not Found please try again with valid email"
    user.password = Hash.bcrypt(request.password)
    db.commit()
    return "Password changed successfully"

@app.get("/get-users", tags=["users"], response_model= list[ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# blog creation section
@app.post("/create-post", tags=['blogs'])
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title= request.title, content= request.content, user_id= request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/get-blogs", tags=['blogs'])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/get-blogs/{user_id}", tags=['blogs'], response_model= list[ShowBlogs])
def get_blogs_by_user_id(user_id: int, db: Session= Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id)
    return blogs


@app.delete("/delete-blogs/{blog_title}", tags=['blogs'])
def delete_blogs(blog_title: str, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.title == blog).delete(synchronize_session= False)
    db.commit()
    return f"The blog with title {blog} has been deleted"

@app.put("/change-blog", tags=['blogs'])
def change_blog_content(request: ShowBlogs, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.title == request.title).update({models.Blog.content: request.content}, synchronize_session= False)
    db.commit()
    return f"Contents of the blog titled {request.title} has been changed successfully"