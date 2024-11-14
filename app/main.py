from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List

# Creamos la aplicación FastAPI
app = FastAPI()

# Definimos el esquema de lectura y respuesta del "Item" usando Pydantic
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None

# Definimos el esquema de creación de un nuevo "Item" sin el campo "id"
class ItemCreate(BaseModel):
    name: str
    description: str | None = None

# Función auxiliar para leer los datos del archivo JSON
def read_data():
    try:
        with open("app/data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Función auxiliar para escribir datos en el archivo JSON
def write_data(data):
    with open("app/data.json", "w") as file:
        json.dump(data, file, indent=4)

# Endpoint para obtener todos los ítems (GET)
@app.get("/items/", response_model=List[Item])
def get_items():
    """
    Devuelve una lista de todos los ítems.
    """
    items = read_data()
    return items

# Endpoint para obtener un ítem específico por su ID (GET)
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """
    Devuelve un ítem específico basado en su ID.
    """
    items = read_data()
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

# Endpoint para crear un nuevo ítem (POST)
@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    """
    Crea un nuevo ítem y lo añade al archivo JSON.
    """
    items = read_data()
    
    # Generar un ID único para el nuevo ítem
    new_id = max([item["id"] for item in items], default=0) + 1
    new_item = item.dict()  # Convertir el ítem a un diccionario
    new_item["id"] = new_id  # Asignar el nuevo ID
    
    # Añadir el nuevo ítem a la lista y guardar
    items.append(new_item)
    write_data(items)
    
    return new_item

# Endpoint para actualizar un ítem existente (PUT)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: ItemCreate):
    """
    Actualiza un ítem existente basado en su ID.
    """
    items = read_data()
    for index, item in enumerate(items):
        if item["id"] == item_id:
            # Actualizar el ítem manteniendo el mismo ID
            items[index] = updated_item.dict()
            items[index]["id"] = item_id  # Mantener el ID original
            write_data(items)
            return items[index]
    raise HTTPException(status_code=404, detail="Item no encontrado")

# Endpoint para eliminar un ítem (DELETE)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """
    Elimina un ítem basado en su ID.
    """
    items = read_data()
    for index, item in enumerate(items):
        if item["id"] == item_id:
            # Eliminar el ítem de la lista
            items.pop(index)
            write_data(items)
            return {"message": "Item eliminado"}
    raise HTTPException(status_code=404, detail="Item no encontrado")