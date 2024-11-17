from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from api.routes.main import api_router
from db.init_db import initialize_database

app = FastAPI()

# try:
#     initialize_database()
# except Exception as e:
#     raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)