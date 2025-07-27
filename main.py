from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

count = 0 # Global counter for item IDs
db = {} # In-memory database to store items

# Sample data model
class Item(BaseModel):
    name: str
    description: str

@app.get("/")
def read_root():    
    return {"message": "Hello World"}

# Get item by ID (fake example)
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# Post a new item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    global count
    count += 1
    db[count] = item
    return db[count]

# Update an existing item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return db[item_id]

# Delete an item
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = db[item_id]
    del db[item_id]
    return deleted_item