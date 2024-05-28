from fastapi import FastAPI, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .crud import create_user, get_user_by_email
from .schemas import UserCreate, UserLoginSchema
from .database import SessionLocal, engine
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import sign_jwt
from .model import User
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
Base.metadata.create_all(bind=engine)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Acesse /docs para visualizar a documentação"}


@app.post("/signup", tags=["user"])
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado")
    user_data = UserCreate(fullname=user.fullname, email=user.email, password=user.password)
    return sign_jwt(create_user(db=db, user_data=user_data).email)

@app.post("/auth", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    print(db_user)
    if db_user and db_user.password == user.password:
        return sign_jwt(db_user.email)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário e/ou senha inválidos")


@app.post("/validate-token", dependencies=[Depends(JWTBearer())], tags=[""])
async def validate_token():
    return {"data": "Token válido"}
