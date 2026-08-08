from passlib.hash import bycrypt 
from passlib.context import CryptContext
pass_context = CryptContext(schemes=["bycrypt"],deprecatted="auto")
def hash_password(password:str)  -> str:
    '''
    it hashes the plain password using bycrypt
    the resultant string will result algorithm,salt and hash.
    '''
    return pass_context.hash(password)
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pass_context.verify(plain_password,hashed_password)