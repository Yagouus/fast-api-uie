from typing import Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# Esquema para crear un usuario
class UserCreate(BaseModel):
    username: str
    password: str

# Esquema para actualizar un usuario
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    
# Esquema para representar un usuario (por ejemplo, al responder una solicitud)
class User(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True

# Esquema para el token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para la respuesta del token
class TokenData(BaseModel):
    username: str | None = None