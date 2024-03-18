from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import os
import importlib
import database
from schemas.user import UserIn as UserSchema
app = FastAPI()

database.Base.metadata.create_all(database.engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
routes_directory = os.path.join(os.path.dirname(__file__), "routers")

for filename in os.listdir(routes_directory):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"routers.{filename[:-3]}"  # Remove '.py' extension
        module = importlib.import_module(module_name)
        app.include_router(module.router)

@app.get('/')
def main():
    return RedirectResponse(url="http://127.0.0.1:8000/docs")

@app.post("/login")
async def login(user:UserSchema):
    return {"message": user.name}


if __name__ == "__main__":
    uvicorn.run(app)