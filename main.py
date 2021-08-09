from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Optional
import requests
import os
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None


@app.post("/", response_model=Item, summary="Create an item", response_description="The created item")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: An API that returns cat pics

    """
    return item


@app.get("/{number}")
async def return_images(number: int):
    dir = "static"
    parent_dir = '/Users/lenguyen/Desktop/ProjectFastAPI'
    path = os.path.join(parent_dir, dir)

    if not os.path.exists(path):
        os.mkdir(path)

    for i in range(number):
        location = os.path.join(path, 'cat' + str(i) + '.jpg')
        r = requests.get('https://cataas.com/cat')
        with open(location, 'wb') as f:
            f.write(r.content)


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    app.run()
