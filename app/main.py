from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, inventory
from .database import Base, engine
from .models import inventory_models, auth_models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(inventory.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory Management API!"}
