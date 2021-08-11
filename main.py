from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional
import requests
import os
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

app = FastAPI(
    title="Cats API",
    description="This API allows users to enter an integer and returns a corresponding number of cat images",
    version="3.0.0",
)

@app.get("/{number}", summary="Number of cat pics returned", description="The API will return a number of cat images")
async def return_images(number: int):
    urls = []
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static")
    for i in range(number):
        location = os.path.join(path, 'cat' + str(i) + '.jpg')
        r = requests.get('https://cataas.com/cat')
        with open(location, 'wb') as f:
            f.write(r.content)
        urls.append("http://127.0.0.1:8000/static/cat" + str(i) + ".jpg")
    return str(urls)
        
app.mount("/static", StaticFiles(directory="static"), name="static")

class Item(BaseModel):
    name: str
    description: Optional[str]
    number: int

@app.post("/", response_model=Item, summary="Cat API")
async def create_item(item: Item):
    """
    FastAPI Project:
    - **name**: Cat pics
    - **description**: This API returns a number of cat images
    - **number**: The number of cat images returned
    """
    return item
    


if __name__ == '__main__':
    app.run()
