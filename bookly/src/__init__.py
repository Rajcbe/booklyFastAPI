from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"

app=FastAPI(title="Bookly", description="Rest API for book review webservcie",version=version)

app.include_router(
    book_router,
    prefix=f'/api/{version}/books',tags=['books'])