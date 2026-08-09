from passlib.hash import bcrypt 
def hash_password(plain_password:str)  -> str:
    """One-directional: produces a hash containing an embedded random
    salt. Never call this to 'check' a password — only to store one."""
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")
def verify_password(plain_password:str, hashed_password: str)->str:
    """Re-hashes the attempt using the salt embedded in hashed_password,
    then compares — this is what actually checks a login, never a
    manual == comparison of two hashes."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )