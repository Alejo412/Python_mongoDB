from fastapi import APIRouter, status, HTTPException
from Backend.FastAPI.db.models.user import User
from Backend.FastAPI.db.schemas.user import user_schema, users_schemas
from Backend.FastAPI.db.client import db_client
from bson import ObjectId



router = APIRouter(prefix="/userdb", tags=["userdb"], responses={status.HTTP_404_NOT_FOUND: {"message":"No encontrado"}})




users_list = []





@router.get("/", response_model=list[User])
async def users():
    return users_schemas(db_client.userss.find())



#PATH
@router.get("/{id}")
async def user(id:str):
    return search_user("_id", ObjectId(id) )


#QUERY
@router.get("/")
async def user(id:str):
    return search_user("_id", ObjectId(id))



@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user:User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario ya existe")
    
    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.userss.insert_one(user_dict)
    new_user = db_client.userss.find_one({"_id":id.inserted_id})
    return User(**user_schema(new_user))



@router.put("/", response_model=User)
async def user(user:User):
    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.userss.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    return search_user("_id",ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.userss.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error":"No se ha eliminado el usuario"}




def search_user(field: str, key):
    try:
        user = db_client.userss.find_one({field:key})
        return User(**user_schema(user)) 
    except:
        return {"error": "No se ha enontrado el usuario"}
    