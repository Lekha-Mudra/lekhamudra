import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession

from app.models.session import Session

SESSION_TTL_HOURS = 24 * 7  # 7 days


def create_session(db: OrmSession, user_id: uuid.UUID) -> Session:
    now = datetime.now(timezone.utc)
    sess = Session(user_id=user_id, expires_at=now + timedelta(hours=SESSION_TTL_HOURS))
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess


def get_session(db: OrmSession, session_id: uuid.UUID) -> Session | None:
    return db.query(Session).filter(Session.id == session_id).first()


def touch_session(db: OrmSession, sess: Session):
    sess.last_used_at = datetime.now(timezone.utc)
    db.add(sess)
    db.commit()


def delete_session(db: OrmSession, sess: Session):
    db.delete(sess)
    db.commit()
