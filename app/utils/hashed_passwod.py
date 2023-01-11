import bcrypt


def hash_password(password: str) -> str:
    """Hashed and return password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_hashed_password(password: str, hashed: str) -> bool:
    """Checking for a password match."""
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        return True
    return False
