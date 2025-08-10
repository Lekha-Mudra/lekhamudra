import uuid
from datetime import datetime, timezone

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_session
from app.db.session import get_db
from app.models.document import Document
from app.models.session import Session as SessionModel
from app.models.user import User


def get_current_user_optional(
    db: Session = Depends(get_db), session_id: str | None = Cookie(default=None)
):
    if not session_id:
        return None
    try:
        sid = uuid.UUID(session_id)
    except ValueError:
        return None
    sess = db.query(SessionModel).filter(SessionModel.id == sid).first()
    if not sess:
        return None
    now = datetime.now(timezone.utc)
    expires_at = sess.expires_at
    if (expires_at.tzinfo is None and expires_at < now.replace(tzinfo=None)) or (
        expires_at.tzinfo is not None and expires_at < now
    ):
        return None
    crud_session.touch_session(db, sess)
    user = db.query(User).filter(User.id == sess.user_id).first()
    return user


def get_current_user(user=Depends(get_current_user_optional)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def get_owned_document(
    doc_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    doc = (
        db.query(Document)
        .filter(Document.id == doc_id, Document.owner_id == current_user.id)
        .first()
    )
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return doc
