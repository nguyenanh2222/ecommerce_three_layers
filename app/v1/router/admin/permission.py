from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from models.permission import Permission

router = APIRouter()
security = HTTPBasic()

@router.get(
    path="/"
)


def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    session: Session = SessionLocal()
    query = session.query(Permission).filter(
        Permission.username.like(f"%{credentials.username}%"
                                 )).filter(
        Permission.password.like(f"{credentials.password}")
    ).scalar()
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"})
    return credentials.username