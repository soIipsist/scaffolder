from fastapi import FastAPI
import uvicorn
import os
import importlib

import database
from schemas.user import User as UserSchema


app = FastAPI()
routes_directory = os.path.join(os.path.dirname(__file__), "routers")

for filename in os.listdir(routes_directory):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"routers.{filename[:-3]}"  # Remove '.py' extension
        module = importlib.import_module(module_name)
        app.include_router(module.router)

@app.get('/')
async def main():
    return {'message': 'hello'}

@app.post("/login")
async def login(user:UserSchema):
    return {"message": user.name}


if __name__ == "__main__":
    uvicorn.run(app)