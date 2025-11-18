from fastapi import FastAPI, HTTPException
from . import crud 

app = FastAPI()

# Rutas 

@app.get("/categorias")
def get_all_categorias_route():
    return crud.get_categorias()

@app.post("/categorias")
def create_categoria_route(nombre: str):
    """
    Llama a la lógica de negocio (CRUD) para crear una categoría.
    """
    return crud.create_categoria_db(nombre)
# agregar esto despues del primer commit
@app.get("/productos")
def get_all_productos_route():
    return crud.get_productos()

@app.post("/productos")
def create_producto_route(nombre: str, categoria_id: int):
    """
    Llama a la lógica de negocio (CRUD) para crear un producto.
    """
    producto = crud.create_producto_db(nombre, categoria_id)
    
    if "error" in producto:
        raise HTTPException(status_code=404, detail=producto["error"])
        
    return producto

@app.put("/productos/{producto_id}")
def update_producto_route(producto_id: int, nombre: str = None, categoria_id: int = None):
    """
    Actualiza un producto por id. Pueden actualizarse nombre y/o categoria_id.
    """
    producto = crud.update_producto_db(producto_id, nombre, categoria_id)
    if isinstance(producto, dict) and "error" in producto:
        raise HTTPException(status_code=404, detail=producto["error"])
    return producto
@app.delete("/productos/{producto_id}")

def delete_producto_route(producto_id: int):
    """
    Elimina un producto por id.
    """
    result = crud.delete_producto_db(producto_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result