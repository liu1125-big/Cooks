from fastapi import FastAPI
from app.api import user, category, dish, recommend, cart, favorite
from app.database.init_db import init_db

app = FastAPI(title="Cooks API", description="Backend API for Cooks application", version="1.0.0")

app.include_router(user.router)
app.include_router(category.router)
app.include_router(dish.router)
app.include_router(recommend.router)
app.include_router(cart.router)
app.include_router(favorite.router)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {"message": "Cooks API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}