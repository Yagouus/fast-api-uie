from app.database import SessionLocal
from app.models import User  # Importa el modelo de SQLAlchemy

# Crear una sesión de base de datos
db = SessionLocal()

# Crear una instancia del modelo `User` (modelo SQLAlchemy)
new_user = User(username="testuser", hashed_password="hashedpassword", is_active=True)

# Añadir el nuevo usuario a la sesión y realizar el commit
db.add(new_user)
db.commit()
db.refresh(new_user)  # Refresca la instancia para actualizar los datos desde la base de datos

# Cerrar la sesión
db.close()