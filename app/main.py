from fastapi import FastAPI, HTTPException, Request, Body
import json
from typing import List, Optional

# Creamos la aplicación FastAPI
app = FastAPI()

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
@app.get("/items/")
def get_items():
    """
    Devuelve una lista de todos los ítems.
    """
    items = read_data()
    return items

# Endpoint para obtener un ítem específico por su ID (GET)
@app.get("/items/{item_id}")
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
@app.post("/items/")
def create_item(item: dict = Body(..., example={"name": "Nuevo Item", "description": "Descripción del nuevo ítem"})):
    """
    Crea un nuevo ítem y lo añade al archivo JSON.
    """
    items = read_data()
    
    # Validación manual de datos
    if "name" not in item or not isinstance(item["name"], str):
        raise HTTPException(status_code=400, detail="El campo 'name' es obligatorio y debe ser una cadena de texto.")
    if "description" in item and not isinstance(item["description"], str):
        raise HTTPException(status_code=400, detail="El campo 'description' debe ser una cadena de texto o estar ausente.")
    
    # Generar un ID único para el nuevo ítem
    new_id = max([item["id"] for item in items], default=0) + 1
    new_item = {
        "id": new_id,
        "name": item["name"],
        "description": item.get("description")  # Añadir descripción si está presente
    }
    
    # Añadir el nuevo ítem a la lista y guardar
    items.append(new_item)
    write_data(items)
    
    return new_item

# Endpoint para actualizar un ítem existente (PUT)
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: dict = Body(..., example={"name": "Item Actualizado", "description": "Descripción actualizada"})):
    """
    Actualiza un ítem existente basado en su ID.
    """
    items = read_data()

    # Validación manual de datos
    if "name" not in updated_item or not isinstance(updated_item["name"], str):
        raise HTTPException(status_code=400, detail="El campo 'name' es obligatorio y debe ser una cadena de texto.")
    if "description" in updated_item and not isinstance(updated_item["description"], str):
        raise HTTPException(status_code=400, detail="El campo 'description' debe ser una cadena de texto o estar ausente.")

    # Buscar y actualizar el ítem
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items[index]["name"] = updated_item["name"]
            items[index]["description"] = updated_item.get("description")
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