from fastapi import  APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username:str
    full_name:str
    email:str
    diseable:bool

class UserDB(User):
    password: str

    
users_db = {
    "Alejo":{
        "username":"Alejo",
        "full_name":"Alejandro Hernandez",
        "email":"alejo@gmail.com",
        "diseable":False,
        "password":"12345"
    }, 
    "Alejo2":{
        "username":"Beto",
        "full_name":"Alejandro Hernandez",
        "email":"alejo@gmail.com",
        "diseable":True,
        "password":"123456"
    }
}

def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username])


async def current_user(token:str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Credenciales de autenticación invalidas",
        headers={"www-Authenticate": "Bearer"})
    return user




@router.post("/login")
async def login(form:OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    print(f"{user_db}{"Este es el print"}")
    if not user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail="El usuario no es correcto")  
    user = search_user(form.username)
    print(f"{user}{"Este es el print 2"}")
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
        detail="La contraseña no es correcta", 
        )  
    return {"acces_token": user.username, "token_type,":"bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user