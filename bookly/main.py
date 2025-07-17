from fastapi import FastAPI,Header,status
from fastapi.exceptions import HTTPException
from typing import Optional,List
from pydantic import BaseModel

app=FastAPI()


class Book(BaseModel):
    id:int
    title: str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str
    
class BookUpdateModel(BaseModel):
    title: str
    author:str
    publisher:str
    page_count:int
    language:str
        
    
books= [
    {
        "id": 1,
        "title": "Python Foundations",
        "author": "Anita Rao",
        "publisher": "CodePress",
        "published_date": "2023-04-12",
        "page_count": 384,
        "language": "en",
    },
    {
        "id": 2,
        "title": "FastAPI in Action",
        "author": "S. Kannan",
        "publisher": "DevPath",
        "published_date": "2024-09-01",
        "page_count": 256,
        "language": "en",
    },
    {
        "id": 3,
        "title": "Data Testing with Python",
        "author": "Pushpa J.",
        "publisher": "QAWorks",
        "published_date": "2022-11-30",
        "page_count": 310,
        "language": "en",
    },
    {
        "id": 4,
        "title": "Django & MySQL Made Simple",
        "author": "R. Murugan",
        "publisher": "Tamil Tech Books",
        "published_date": "2021-06-20",
        "page_count": 428,
        "language": "ta",
    },
    {
        "id": 5,
        "title": "ETL Pipelines with PySpark",
        "author": "Neha Gupta",
        "publisher": "DataCraft",
        "published_date": "2024-01-15",
        "page_count": 512,
        "language": "en",
    },
]    

@app.get("/")
async def read_root():
    return {"message":"Hello, World!"}


@app.get('/books',response_model=List[Book])
async def get_all_books():
    return books


@app.post('/books',status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book)->dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.get('/books/{book_id}', response_model=Book)
async def get_book_by_id(book_id: int)->dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"    
    )

@app.patch('/books/{book_id}', response_model=Book)
async def update_book(book_id: int,book_update_data:BookUpdateModel)->dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language
            return book
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )
    
    
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)    
async def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            
            return {}
            
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {book_id} not found"
    )
    
@app.get('/headers')
async def get_headers(
    accept:str=Header(None),
    content_type = Header(None)
):
    request_headers = {}
    request_headers['Accept'] = accept
    request_headers['Content-Type'] = content_type  
    return request_headers