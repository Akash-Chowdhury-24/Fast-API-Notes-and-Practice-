from pydantic import BaseModel
from fastapi import APIRouter, Depends
from controllers import (
  get_all_books,
  get_single_book,
  create_book,
  update_book,
  delete_book,
  APIResponseModel
)
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from fastapi import status

router = APIRouter(prefix="/books", tags=["Books"])

class BookModel(BaseModel):
    title: str
    author: str
    description: str
    
class BookResponseModel(BaseModel):
    id: str
    title: str  
    author: str
    description: str



@router.get("/", response_model=APIResponseModel[List[BookResponseModel]])
def read_all_books(db:Session = Depends(get_db)):
    return get_all_books(db)


@router.get("/{book_id}", response_model=APIResponseModel[BookResponseModel])
def read_single_book( book_id :str, db : Session = Depends(get_db)):
    return get_single_book(db, book_id)
  
@router.post("/", response_model=APIResponseModel[BookResponseModel], status_code=status.HTTP_201_CREATED)
def create_new_book(book: BookModel, db:Session = Depends(get_db)):
    return create_book(db, book)
  
@router.put("/{book_id}", response_model=APIResponseModel[BookResponseModel])
def update_existing_book(book:BookModel, book_id:str, db:Session = Depends(get_db)):
    return update_book(db, book_id, book)
  

@router.delete("/{book_id}", response_model=APIResponseModel[None])
def delete_existing_book(book_id:str, db:Session = Depends(get_db)):
    return delete_book(db, book_id)