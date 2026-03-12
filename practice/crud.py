
from fastapi import FastAPI , status
from pydantic import BaseModel
from typing import TypeVar, Generic, Dict
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4


app = FastAPI()


booksData : Dict[str,dict] ={}
T = TypeVar("T")

class APIResponseModel(BaseModel, Generic[T]):
  success: bool
  message: str
  data: T
class BookModel(BaseModel):
  title: str
  author: str
  description: str
  
class BookResponseModel(BaseModel):
  id:str
  title: str
  author: str
  description: str
  
  
@app.exception_handler(HTTPException)
def http_exception_handler(request:Request, exc:HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "success": False,
      "message": exc.detail,
      "data": None
    }
  )


@app.get("/books", response_model=APIResponseModel[list[BookResponseModel]])
def get_all_books():
  return APIResponseModel(
    success=True,
    message="Books retrieved successfully",
    data= list(booksData.values())
  )
  
@app.get("/books/{book_id}", response_model=APIResponseModel[BookResponseModel])
def get_book(book_id:str):
  book = booksData.get(book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  return APIResponseModel(
    success=True,
    message="Book retrieved successfully",
    data=book
  )
  
@app.post("/books", response_model=APIResponseModel[BookResponseModel], status_code=status.HTTP_201_CREATED)
def create_book(book:BookModel):
  new_book_id = str(uuid4())
  new_book = {
    "id": new_book_id,
    "title": book.title,
    "author": book.author,
    "description": book.description
  }
  booksData[new_book_id] = new_book
  return APIResponseModel(
    success=True,
    message="Book created successfully",
    data=new_book
  )
  

@app.put("/books/{book_id}", response_model=APIResponseModel[BookResponseModel])
def update_book(book_id:str, book:BookModel):
  
  if book_id not in booksData:
    raise HTTPException(status_code=404, detail="Book not found")
  
  updated_book = {
    "id": book_id,
    "title": book.title,
    "author": book.author,
    "description": book.description
  }
  
  booksData[book_id] = updated_book
  return APIResponseModel(
    success=True,
    message="Book updated successfully",
    data=updated_book
  )
  

@app.delete("/books/{book_id}",response_model=APIResponseModel[None])
def delete_book(book_id:str):
  if book_id not in booksData:
    raise HTTPException(status_code=404, detail="Book not found")
  del booksData[book_id]
  return APIResponseModel(
    success=True,
    message="Book deleted successfully",
    data=None
  )