import uvicorn
from fastapi import FastAPI
from src.routers import controllers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(controllers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)