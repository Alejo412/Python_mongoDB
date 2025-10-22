from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class User(BaseModel):
    id:int
    name:str
    surname:str
    url:str
    age:int

users_list = [User(id=1, name="Alejo",surname="Hernandez", url="https://alejo.dev", age=20),
    User(id=2, name="Brayan",surname="Romero", url="https://romero.dev", age=20),
    User(id=3, name="Marde",surname="Puentes", url="https://marde.dev", age=20)]


@router.get("/users_json")
async def users():
    return [{"name":"Alejo", "surname":"Hernandez", "url":"https://alejo.dev", "age":20},
        {"name":"Brayan", "surname":"Romero", "url":"https://brayan.dev", "age":20},
        {"name":"Marde", "surname":"Puentes", "url":"https://marde.dev", "age":20}]




@router.get("/users/")
async def users():
    return users_list



#PATH
@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)


#QUERY
@router.get("/userquery/")
async def user(id:int):
    return search_user(id)



@router.post("/user/", status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204,detail="El usuario ya existe")  
        
    users_list.routerend(user)
    return user



@router.put("/user/")
async def user(user:User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    
    return user


@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error":"No se ha eliminado el usuario"}


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha enontrado el usuario"}
    