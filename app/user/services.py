import logging
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError, IntegrityError 

from app.config.cnx import SessionLocal
from app.config.sql_models import User
from app.user.dto import UserCreateDTO, UserInsertDTO, UserUpdateDTO
from app.middlewares.auth import hash_password, compare_password, create_access_token

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_user_by_id(user_id: int):
    """Ejecuta una busqueda para encontrar en la table usuarios un registro
    que corresponda con el id y no este borrado de manera logica."""
    with SessionLocal() as db:
        return (
            db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
        )


def get_user_by_email(email: str):
    """Busca y retorna el primer registro que coincida con el campo email."""
    with SessionLocal() as db:
        return db.query(User).filter(User.email == email).first()


def get_all_users():
    """Busca y retorna todos los usuarios activos."""
    with SessionLocal() as db:
        users = db.query(User).filter(User.deleted_at.is_(None)).all()
        return users


def create_user(user_data: UserCreateDTO):
    """Crea y retorna el registro de usuario si se ejecuta de manera exitosa."""
    
    hashed = hash_password(user_data.password)
    new_user = User(
        name=user_data.name.strip(),
        email=user_data.email.strip().lower(),
        password=hashed,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    try:
        with SessionLocal() as db:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(
                "Created new user with id %s and email %s", new_user.id, new_user.email
            )
            return new_user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while creating user %s: %s",
            new_user.email,
            e,
            exc_info=True,
        )
        raise


def insert_user(user_data: UserInsertDTO):
    """Insertar un usuario con datos predefinidos (para seeders)"""
    db = None
    try:
        db = SessionLocal()
        
        # Verificar si ya existe
        existing_user = db.query(User).filter(User.id == user_data.id).first()
        if existing_user:
            logger.info(f"Usuario {user_data.id} ya existe, saltando inserción")
            return existing_user
        
        # Crear el usuario
        user = User(
            id=user_data.id,
            firstName=user_data.firstName.strip(),
            lastName=user_data.lastName.strip(),
            email=user_data.emails.strip().lower(),
            password=user_data.password,  # Ya debe venir hasheado
            ages=user_data.ages,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario insertado exitosamente: ID {user.id}, Email: {user.email}")
        return user
        
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al insertar usuario: {str(e)}")
        raise IntegrityError("Error de datos duplicados", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al insertar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al insertar usuario: {str(e)}")
        raise Exception("Error interno al insertar el usuario")
    finally:
        if db:
            db.close()


def update_user(user_id: str, user_data: UserUpdateDTO):
    """Actualizar un usuario existente"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado para actualizar")
            raise ValueError("Usuario no encontrado")
        
        # Actualizar campos si se proporcionan
        if user_data.firstName:
            user.firstName = user_data.firstName.strip()
        if user_data.lastName:
            user.lastName = user_data.lastName.strip()
        if user_data.email:
            # Validar que el nuevo email no exista en otro usuario
            existing_user = db.query(User).filter(
                User.email == user_data.email.strip().lower(),
                User.id != user_id
            ).first()
            if existing_user:
                logger.warning(f"Intento de actualizar con email existente: {user_data.email}")
                raise ValueError("El email ya está registrado")
            user.email = user_data.email.strip().lower()
        if user_data.password:
            user.password = hash_password(user_data.password)
        if user_data.ages is not None:
            user.ages = user_data.ages
            
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario {user_id} actualizado exitosamente")
        return user
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except IntegrityError as e:
        if db:
            db.rollback()
        logger.error(f"Error de integridad al actualizar usuario: {str(e)}")
        raise IntegrityError("Email ya está registrado", None, e)
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al actualizar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al actualizar usuario: {str(e)}")
        raise Exception("Error interno al actualizar el usuario")
    finally:
        if db:
            db.close()


def soft_delete_user(user_id: int):
    """Borra de manera logica el registro de un usuario activo."""
    try:
        with SessionLocal() as db:
            user = db.get(User, user_id)

            if not user:
                return None

            user.deleted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)

            logger.info("Soft-deleted user with id %s", user_id)
            return user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while soft-deleting user %s: %s", user_id, e, exc_info=True
        )
        raise


def hard_delete_user(user_id: int):
    """Borra de manera PERMANENTE un registro en la base de datos."""
    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None

            db.delete(user)
            db.commit()
            logger.info("Hard-deleted user with id %s", user_id)
            return user

    except SQLAlchemyError as e:
        logger.error(
            "Database error while hard-deleting user %s: %s", user_id, e, exc_info=True
        )
        raise


def authenticate_user(email: str, password: str):
    """Autenticar un usuario por email y contraseña"""
    db = None
    try:
        if not email or not password:
            return None
            
        db = SessionLocal()
        user = db.query(User).filter(
            User.email == email.strip().lower(),
            User.deleted_at == None
        ).first()
        
        if not user or not compare_password(password, user.password):
            logger.warning(f"Intento de autenticación fallido para email: {email}")
            return None
            
        logger.info(f"Usuario autenticado exitosamente: {user.email}")
        return user
        
    except Exception as e:
        logger.error(f"Error inesperado al autenticar usuario: {str(e)}")
        return None
    finally:
        if db:
            db.close()


def restore_user(user_id: str):
    """Restaurar un usuario eliminado lógicamente"""
    db = None
    try:
        if not user_id or not user_id.strip():
            raise ValueError("ID de usuario requerido")
            
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id, User.deleted_at != None).first()
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado en eliminados")
            raise ValueError("Usuario eliminado no encontrado")
        
        user.deleted_at = None
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)
        
        logger.info(f"Usuario {user_id} restaurado exitosamente")
        return user
        
    except ValueError:
        if db:
            db.rollback()
        raise
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Error de base de datos al restaurar usuario: {str(e)}")
        raise SQLAlchemyError("Error al acceder a la base de datos")
    except Exception as e:
        if db:
            db.rollback()
        logger.error(f"Error inesperado al restaurar usuario: {str(e)}")
        raise Exception("Error interno al restaurar el usuario")
    finally:
        if db:
            db.close()


def login_user(email: str, password: str):
    """Login de usuario y generación de token"""
    user = authenticate_user(email, password)
    if not user:
        raise ValueError("Credenciales inválidas")
    
    # Generar token
    token_data = {
        "sub": user.email,
        "user_id": str(user.id),
        "firstName": getattr(user, "firstName", ""),
        "lastName": getattr(user, "lastName", "")
    }
    
    access_token = create_access_token(data=token_data)
    
    logger.info(f"Login exitoso para usuario: {user.email}")
    return {
        "access_token": access_token,
        "token_type": "bearer", 
        "user_id": str(user.id),
        "user_email": user.email
    }