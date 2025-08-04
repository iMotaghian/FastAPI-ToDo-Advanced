from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic,HTTPBasicCredentials,HTTPAuthorizationCredentials,HTTPBearer
from users.models import UserModel,TokenModel
from core.database import get_db
from sqlalchemy.orm import Session

security = HTTPBearer(scheme_name="Token")


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):  
    token_obj = db.query(TokenModel).filter_by(token=credentials.credentials).one_or_none()
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )
        
    return token_obj.user