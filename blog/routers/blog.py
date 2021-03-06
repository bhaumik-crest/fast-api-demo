from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.DisplayBlog,
)
def create(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        published=request.published,
        user_id=current_user.id,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/", response_model=List[schemas.DisplayBlog])
def all(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DisplayBlog,
)
def one(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def remove(
    id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
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
