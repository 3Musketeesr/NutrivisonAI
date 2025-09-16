from fastapi import FastAPI 

app = FastAPI()


@app.get("/")
async def testing():
    return {"hello": "world"}