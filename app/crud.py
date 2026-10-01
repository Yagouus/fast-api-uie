from sqlalchemy.orm import Session
<<<<<<< Updated upstream
from . import models, schemas
=======
from .models import User, Item
from . import schemas
from passlib.context import CryptContext
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Obtener usuario por nombre de usuario
def get_user_by_username(db: Session, username: str):
    try:
        logger.info(f"Searching user with username: {username}")
        user = db.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        logger.error(f"Error during user search: {e}")
        raise

# Crear un nuevo usuario
def create_user(db: Session, user: schemas.UserCreate):
    print(repr(user.password), type(user.password), len(user.password.encode()))
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Obtener todos los usuarios con paginación
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

# Obtener usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Actualizar usuario
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.username:
            db_user.username = user.username
        if user.password:
            db_user.hashed_password = get_password_hash(user.password)
        if user.is_active is not None:
            db_user.is_active = user.is_active
        db.commit()
        db.refresh(db_user)
    return db_user
>>>>>>> Stashed changes

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()
    
def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True