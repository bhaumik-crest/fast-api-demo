from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt(password: str):
    return pwd_context.hash(password)


def verify(password: str, hash_password: str):
    return pwd_context.verify(password, hash_password)
