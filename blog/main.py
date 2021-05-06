from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from . import schemas, models
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, body=request.body, published=request.published
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.DisplayBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get(
    "/blog/{id}", status_code=status.HTTP_200_OK, response_model=schemas.DisplayBlog
)
def one(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog


@app.delete(
    "/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
def remove(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    db.commit()


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    try:
        blog.update(
            {
                "title": request.title,
                "body": request.body,
                "published": request.published,
            }
        )
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return "updated"
