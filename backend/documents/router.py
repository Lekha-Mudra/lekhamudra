from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from documents.schemas import Document as DocumentSchema
from documents.models import Document as DocumentModel
from database import get_db
from auth.security import get_current_user
from auth.models import User

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/", response_model=List[DocumentSchema])
def list_docs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DocumentModel).filter(DocumentModel.owner == current_user.email).all()

@router.post("/", response_model=DocumentSchema)
def create_doc(doc: DocumentSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_doc = DocumentModel(
        title=doc.title,
        content=doc.content,
        owner=current_user.email,
        last_modified=datetime.utcnow().isoformat()
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.get("/{doc_id}", response_model=DocumentSchema)
def get_doc(doc_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc or doc.owner != current_user.email:
        raise HTTPException(status_code=404, detail="Not found or no access")
    return doc

@router.put("/{doc_id}", response_model=DocumentSchema)
def update_doc(doc_id: int, doc_update: DocumentSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc or doc.owner != current_user.email:
        raise HTTPException(status_code=404, detail="Not found or no access")
        
    doc.title = doc_update.title
    doc.content = doc_update.content
    doc.last_modified = datetime.utcnow().isoformat()
    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}")
def delete_doc(doc_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    doc = db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()
    if not doc or doc.owner != current_user.email:
        raise HTTPException(status_code=404, detail="Not found or no access")
        
    db.delete(doc)
    db.commit()
    return {"ok": True}
