# FastAPI Project

Este proyecto es una API REST básica creada con FastAPI. Implementa operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para un recurso de ejemplo (`Item`), utilizando SQLAlchemy para manejar la persistencia de datos y Pydantic para la validación de esquemas.

### Requisitos

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Databases
- SQLite (opcional, para la base de datos local)

### Configuración del Proyecto

#### Paso 1: Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd fastapi_project
```

### Paso 2: Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Para Linux/Mac
venv\Scripts\activate      # Para Windows
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la API
```bash
uvicorn app.main:app --reload
```

### Documentación de la API

FastAPI genera la documentación automáticamente. Puedes acceder a ella en:

	- Swagger UI: http://127.0.0.1:8000/docs
	- Redoc: http://127.0.0.1:8000/redoc
