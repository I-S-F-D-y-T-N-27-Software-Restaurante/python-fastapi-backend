from fastapi import FastAPI
# import sqlalchemy

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
