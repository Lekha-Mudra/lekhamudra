from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional
from app.core.security import verify_password
from app.crud import crud_session, crud_user
from app.db.session import get_db
from app.schemas.user import User, UserCreate

router = APIRouter()

SESSION_COOKIE_NAME = "session_id"


def _set_session_cookie(response: Response, session_id: str):
    response.set_cookie(
        SESSION_COOKIE_NAME,
        session_id,
        httponly=True,
        samesite="lax",
        secure=False,  # set True in production over HTTPS
        path="/",
    )


@router.post("/signup", response_model=User, status_code=201)
def signup(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    if crud_user.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud_user.create_user(db, user_in)
    sess = crud_session.create_session(db, user.id)
    _set_session_cookie(response, str(sess.id))
    return user


@router.post("/login", response_model=User)
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud_user.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    sess = crud_session.create_session(db, user.id)
    _set_session_cookie(response, str(sess.id))
    return user


@router.post("/logout")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    sid = request.cookies.get(SESSION_COOKIE_NAME)
    if sid:
        from uuid import UUID

        try:
            uuid_sid = UUID(sid)
            from app.models.session import Session as SessionModel

            sess = db.query(SessionModel).filter(SessionModel.id == uuid_sid).first()
            if sess:
                from app.crud import crud_session as cs

                cs.delete_session(db, sess)
        except Exception:
            pass
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"ok": True}


@router.get("/me")
def me(current_user=Depends(get_current_user_optional)):
    if not current_user:
        return {"authenticated": False, "user": None}
    return {
        "authenticated": True,
        "user": {
            "id": str(current_user.id),
            "email": current_user.email,
            "full_name": current_user.full_name,
        },
    }
