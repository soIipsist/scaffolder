from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

import fastapi_template.database as database
from fastapi_template.schemas.user import UserIn as UserSchema
from fastapi_template.models.user import Base as user_base

from fastapi_template.routers.user import router as user_router
from fastapi_template.routers.post import router as post_router

app = FastAPI()
user_base.metadata.create_all(database.engine)
# post_base.Base.metadata.create_all(database.engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(post_router)


@app.get("/")
def main():
    return RedirectResponse(url="http://127.0.0.1:8000/docs")


@app.post("/login")
async def login(user: UserSchema):
    return {"message": user.name}


if __name__ == "__main__":
    uvicorn.run(app)
