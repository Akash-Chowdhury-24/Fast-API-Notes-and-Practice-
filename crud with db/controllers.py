
from pydantic import BaseModel
from typing import TypeVar, Generic
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from uuid import uuid4
import model



T = TypeVar("T")

class APIResponseModel(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T
    

def http_exception_handler(request:Request, exc:HTTPException):
    return JSONResponse(
      status_code=exc.status_code,
      content={
        "success": False,
        "message": exc.detail,
        "data": None
      }
    )
    

def get_all_books(db:Session):
    books = db.query(model.Book).all()
    return APIResponseModel(
      success=True,
      message="Books retrieved successfully",
      data=books
    )
    
def get_single_book(db:Session, book_id:str):
  book = db.query(model.Book).filter(model.Book.id == book_id).first()
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  
  return APIResponseModel(
    success=True,
    message="Book retrieved successfully",
    data=book
  )


def create_book(db:Session, book_data):
  new_book = model.Book(
    id = str(uuid4()),
    title = book_data.title,
    author = book_data.author,
    description = book_data.description
  )
  
  db.add(new_book)
  db.commit()
  db.refresh(new_book)
  
  return APIResponseModel(
    success=True,
    message="Book created successfully",
    data=new_book
  )
  
def update_book(db:Session, book_id:str, book_data):
  book = db.query(model.Book).filter(model.Book.id == book_id).first()
  
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  
  book.title = book_data.title
  book.author = book_data.author
  book.description = book_data.description
  
  db.commit()
  db.refresh(book)
  
  return APIResponseModel(
    success=True,
    message="Book updated successfully",
    data=book
  )
  
  
def delete_book(db:Session , book_id:str):
  book = db.query(model.Book).filter(model.Book.id == book_id).first()
  
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  
  db.delete(book)
  db.commit()
  
  return APIResponseModel(
    success=True,
    message="Book deleted successfully",
    data=None
  )