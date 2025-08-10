import uuid

from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


def get_documents_for_owner(db: Session, owner_id: uuid.UUID) -> list[Document]:
    return db.query(Document).filter(Document.owner_id == owner_id).all()


def create_document(db: Session, owner_id: uuid.UUID, doc_in: DocumentCreate) -> Document:
    doc = Document(title=doc_in.title, content=doc_in.content, owner_id=owner_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_document(db: Session, doc_id: uuid.UUID) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id).first()


def update_document(db: Session, doc: Document, doc_in: DocumentUpdate) -> Document:
    updated_fields = doc_in.dict(exclude_unset=True)
    for field, value in updated_fields.items():
        setattr(doc, field, value)
    doc.version = doc.version + 1
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def delete_document(db: Session, doc: Document) -> None:
    db.delete(doc)
    db.commit()
