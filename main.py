from fastapi import FastAPI, HTTPException
from models import Sheep
from models.db import db

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep

@app.post("/sheep", response_model=Sheep, status_code=201)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")
    db.data[sheep.id] = sheep
    return sheep

# Delete a sheep by ID
@app.delete("/sheep/{id}", status_code=204)
def delete_sheep(id: int):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    del db.data[id]
    return None  # 204 No Content doesn't require a response body

# Update a sheep by ID
@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, updated_sheep: Sheep):
    if id not in db.data:
        raise HTTPException(status_code=404, detail="Sheep not found")
    db.data[id] = updated_sheep
    return updated_sheep

# Read all sheep
@app.get("/sheep", response_model=list[Sheep])
def read_all_sheep():
    return list(db.data.values())
