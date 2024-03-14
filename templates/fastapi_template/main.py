from fastapi import FastAPI
import uvicorn
import os
import importlib

app = FastAPI()


routes_directory = os.path.join(os.path.dirname(__file__), "routers")

for filename in os.listdir(routes_directory):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"routers.{filename[:-3]}"  # Remove '.py' extension
        module = importlib.import_module(module_name)
        app.include_router(module.router)


@app.get("/login")
async def login():
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port='8080')