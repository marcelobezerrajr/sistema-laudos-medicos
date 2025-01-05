from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info("A verificação da senha foi bem-sucedida.")
        return result
    except Exception as e:
        logger.error(f"Falha na verificação da senha: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    try:
        hashed = pwd_context.hash(password)
        logger.info("Hash de senha bem-sucedido.")
        return hashed
    except Exception as e:
        logger.error(f"Falha no hash da senha: {str(e)}")
        raise
