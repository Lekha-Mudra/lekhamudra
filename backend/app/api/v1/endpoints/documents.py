from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_document
from app.db.session import get_db
from app.schemas.document import Document, DocumentCreate, DocumentUpdate

router = APIRouter()


@router.get("/", response_model=list[Document])
def list_documents(db: Session = Depends(get_db), current_user=Depends(deps.get_current_user)):
    return crud_document.get_documents_for_owner(db, owner_id=current_user.id)


@router.post("/", response_model=Document, status_code=201)
def create_document(
    doc_in: DocumentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(deps.get_current_user),
):
    return crud_document.create_document(db, owner_id=current_user.id, doc_in=doc_in)


@router.get("/{doc_id}", response_model=Document)
def get_document(doc=Depends(deps.get_owned_document)):
    return doc


@router.put("/{doc_id}", response_model=Document)
def update_document(
    doc_in: DocumentUpdate,
    db: Session = Depends(get_db),
    doc=Depends(deps.get_owned_document),
):
    return crud_document.update_document(db, doc, doc_in)


@router.delete("/{doc_id}")
def delete_document(db: Session = Depends(get_db), doc=Depends(deps.get_owned_document)):
    crud_document.delete_document(db, doc)
    return {"ok": True}
