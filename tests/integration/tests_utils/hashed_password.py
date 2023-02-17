import bcrypt


def hash_password(password: str) -> str:
    """Hashed and return password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
