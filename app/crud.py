import json
from typing import Dict, Any, List

DB_FILE = "app/db.json"

def _load_db() -> Dict[str, Any]:
    """Carga los datos del archivo JSON."""
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"categorias": [], "productos": []}

def _save_db(db_data: Dict[str, Any]):
    """Guarda los datos en el archivo JSON."""
    with open(DB_FILE, 'w') as f:
        json.dump(db_data, f, indent=2)

def get_categorias() -> List[dict]:
    return _load_db().get("categorias", [])

def get_productos() -> List[dict]:
    return _load_db().get("productos", [])

def create_categoria_db(nombre: str) -> dict:
    """
    PRUEBA UNITARIA: Lógica para crear una nueva categoría.
    Aislamiento perfecto.
    """
    db = _load_db() 
    
    # ID incremental
    new_id = max([c.get('id', 0) for c in db['categorias']] or [0]) + 1
    new_categoria = {"id": new_id, "nombre": nombre}
    
    db['categorias'].append(new_categoria)
    _save_db(db)
    return new_categoria

def create_producto_db(nombre: str, categoria_id: int) -> dict:
    """
    PRUEBA INTEGRACIÓN: Lógica para crear un producto, verificando existencia.
    """
    db = _load_db()

    # Verificación de Integridad
    if not any(c['id'] == categoria_id for c in db['categorias']):
        return {"error": "Categoría no encontrada"}

    new_id = max([p.get('id', 100) for p in db['productos']] or [100]) + 1
    new_producto = {"id": new_id, "nombre": nombre, "categoria_id": categoria_id}
    
    db['productos'].append(new_producto)
    _save_db(db)
    return new_producto

def update_producto_db(producto_id: int, nombre: str = None, categoria_id: int = None) -> dict:
    """
    Actualiza un producto existente. Verifica existencia de producto y categoría (si se cambia).
    Devuelve el producto actualizado o un dict con "error".
    """
    db = _load_db()

    # Buscar producto
    for producto in db.get('productos', []):
        if producto.get('id') == producto_id:
            # Si se solicita cambiar categoría, verificar que exista
            if categoria_id is not None and not any(c['id'] == categoria_id for c in db.get('categorias', [])):
                return {"error": "Categoría no encontrada"}

            # Actualizar campos si se proporcionaron
            if nombre is not None:
                producto['nombre'] = nombre
            if categoria_id is not None:
                producto['categoria_id'] = categoria_id

            _save_db(db)
            return producto

    return {"error": "Producto no encontrado"}

def delete_producto_db(producto_id: int) -> dict:
    """
    Elimina un producto por su ID.
    Devuelve el producto eliminado o un dict con "error" si no se encuentra.
    """
    db = _load_db()
    for idx, producto in enumerate(db.get('productos', [])):
        if producto.get('id') == producto_id:
            eliminado = db['productos'].pop(idx)
            _save_db(db)
            return eliminado
    return {"error": "Producto no encontrado"}