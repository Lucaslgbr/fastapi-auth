from fastapi import FastAPI, Body, Depends

from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from app.model import UserSchema, UserLoginSchema
from fastapi.middleware.cors import CORSMiddleware


users = []

app = FastAPI()

origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# helpers

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Acesse /docs para visualizar a documentação"}


@app.post("/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return sign_jwt(user.email)


@app.post("/auth", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return sign_jwt(user.email)
    return {
        "error": "Usuário e/ou senha inválidos"
    }


@app.post("/validate-token", dependencies=[Depends(JWTBearer())], tags=[""])
async def validate_token():
    return {
        "data": "Token válido"
    }


