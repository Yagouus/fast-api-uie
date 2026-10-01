# API REST de ejemplo con FastAPI

Este repositorio contiene un backend didáctico con una API REST para gestionar elementos (`Item`). Sirve para ver cómo definir endpoints HTTP, dar tipos a los datos de entrada y salida con Pydantic, organizar operaciones CRUD y persistir información usando SQLAlchemy y SQLite.

La aplicación es un único servicio FastAPI organizado en módulos. No es una arquitectura de microservicios distribuida: el ejemplo no separa funcionalidades en procesos desplegables de forma independiente.

## Qué incluye

- Crear, listar, consultar, actualizar y eliminar elementos.
- Validación y serialización de datos con esquemas Pydantic.
- Persistencia local con SQLAlchemy y SQLite en el archivo `test.db`.
- Documentación OpenAPI generada automáticamente por FastAPI.

## Cómo se organiza una petición

```text
Cliente (Swagger, Postman o frontend)
          |
          v
app/main.py       Rutas HTTP y códigos de respuesta
          |
          v
app/schemas.py    Validación y formato de entrada y salida (Pydantic)
          |
          v
app/crud.py       Consultas y operaciones CRUD
          |
          v
app/models.py     Modelo ORM Item (SQLAlchemy)
          |
          v
app/database.py   Sesiones y conexión con SQLite (test.db)
```

`main.py` obtiene una sesión de base de datos mediante una dependencia de FastAPI y pasa los datos validados a las funciones de `crud.py`. Los esquemas describen los datos de la API y los modelos ORM describen cómo se guardan. Separarlos ayuda a mantener las rutas, la validación y el acceso a datos con responsabilidades claras.

## Estructura

```text
app/
├── main.py       Aplicación FastAPI y endpoints
├── schemas.py    Esquemas Pydantic para peticiones y respuestas
├── models.py     Modelo SQLAlchemy Item
├── database.py   Motor, sesiones y base declarativa de SQLite
└── crud.py       Operaciones de acceso y modificación de elementos
requirements.txt  Dependencias Python
```

## Bibliotecas y herramientas

### FastAPI: la interfaz HTTP

[FastAPI](https://fastapi.tiangolo.com/) es el framework que recibe las peticiones y las dirige a una función según la ruta y el método HTTP. En `app/main.py`, decoradores como `@app.get("/items/")` definen los endpoints; `Depends(get_db)` proporciona una sesión de base de datos a cada operación y `HTTPException` permite responder con un error `404` cuando no existe un elemento.

El parámetro `response_model=schemas.Item` indica la estructura de la respuesta. FastAPI lo usa para validar y serializar el resultado y para describirlo en OpenAPI. Así, el contrato HTTP queda visible en `/docs` sin escribir esa documentación por separado. Referencias: [dependencias](https://fastapi.tiangolo.com/tutorial/dependencies/) y [modelos de respuesta](https://fastapi.tiangolo.com/tutorial/response-model/).

### Pydantic: tipado y validación de datos

[Pydantic](https://docs.pydantic.dev/latest/concepts/models/) se usa para el **tipado de datos de la API**. Sus modelos heredan de `BaseModel` y declaran los campos mediante anotaciones de tipos de Python. Por ejemplo, en `app/schemas.py`:

```python
class ItemBase(BaseModel):
    name: str
    description: str | None = None
```

`name: str` declara un campo obligatorio cuyo tipo esperado es texto. `description: str | None = None` permite texto o `None` y tiene un valor predeterminado, por lo que puede omitirse. Las anotaciones expresan los tipos; Pydantic las utiliza para comprobar los datos en tiempo de ejecución y, cuando es posible, convertirlos al tipo esperado. FastAPI usa ese modelo para validar el cuerpo de las peticiones.

`ItemCreate` y `ItemUpdate` describen los datos recibidos. `Item` añade `id: int` para las respuestas. Como `ItemUpdate` hereda de `ItemBase`, el nombre también es obligatorio al actualizar. Estos esquemas describen datos que viajan por la API; la tabla de la base de datos se define por separado con SQLAlchemy. Referencias: [modelos Pydantic](https://docs.pydantic.dev/latest/concepts/models/) y [cuerpos de petición en FastAPI](https://fastapi.tiangolo.com/tutorial/body/).

### SQLAlchemy: acceso a la base de datos

[SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/) es la biblioteca ORM (*mapeo objeto-relacional*): relaciona la clase Python `Item` de `app/models.py` con la tabla `items`. En `app/database.py` crea el motor de conexión y la fábrica `SessionLocal`; `get_db()` abre una sesión para la petición y la cierra al terminar.

Las funciones de `app/crud.py` usan esa sesión para consultar, añadir, modificar o borrar elementos. Después de un cambio llaman a `commit()` para guardarlo; `refresh()` recupera los valores generados por la base, como el identificador. Esto mantiene las consultas fuera de los endpoints. Referencias: [introducción al ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) y [uso de sesiones](https://docs.sqlalchemy.org/en/20/orm/session_basics.html).

### SQLite: almacenamiento local

[SQLite](https://www.sqlite.org/about.html) es el motor de base de datos relacional que guarda los datos en el archivo `test.db`. La URL `sqlite:///./test.db` de `app/database.py` indica a SQLAlchemy dónde abrir ese archivo. Se usa porque funciona [sin instalar ni administrar un servidor de base de datos independiente](https://sqlite.org/serverless.html).

### Uvicorn: ejecución de la aplicación

[Uvicorn](https://www.uvicorn.org/) es el servidor ASGI que ejecuta la aplicación FastAPI y atiende las conexiones HTTP. En `uvicorn app.main:app --reload`, `app.main:app` señala la instancia `app` del módulo `app/main.py`; `--reload` reinicia el servidor al cambiar el código durante el desarrollo. [Referencia: opciones de ejecución de Uvicorn](https://www.uvicorn.org/settings/).

### Dependencia listada que no se utiliza

El `requirements.txt` de `main` también incluye [Databases](https://www.encode.io/databases/), una biblioteca para consultas asíncronas. Este proyecto no la importa: el acceso a SQLite se hace con sesiones síncronas de SQLAlchemy.

## Preparar y ejecutar

Se necesita Python 3.10 o posterior. Desde la raíz del repositorio, crea y activa un entorno virtual:

```bash
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Instala las dependencias e inicia el servidor:

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`. Al iniciar, crea la tabla del modelo si todavía no existe. SQLite guarda los datos en `test.db`, en el directorio desde el que se ejecuta Uvicorn.

## Probar la API

Abre `http://127.0.0.1:8000/docs` para probar los endpoints con Swagger UI o `http://127.0.0.1:8000/redoc` para consultar ReDoc.

| Método | Ruta | Uso |
| --- | --- | --- |
| `POST` | `/items/` | Crear un elemento |
| `GET` | `/items/` | Listar elementos; admite `skip` y `limit` |
| `GET` | `/items/{item_id}` | Consultar un elemento por su identificador |
| `PUT` | `/items/{item_id}` | Actualizar un elemento |
| `DELETE` | `/items/{item_id}` | Eliminar un elemento |

Si el identificador no existe, las rutas de consulta, actualización y borrado devuelven `404`.

## Nota sobre Pydantic

El esquema ORM de `app/schemas.py` en `main` usa `orm_mode = True`, configuración propia de Pydantic 1. Como su `requirements.txt` no fija versiones, `pip install` puede instalar Pydantic 2. En esa versión, la opción se llama `from_attributes` y puede declararse con `model_config = ConfigDict(from_attributes=True)`. Consulta la [guía oficial de migración](https://docs.pydantic.dev/latest/migration/#changes-to-config) al elegir la versión de Pydantic.
