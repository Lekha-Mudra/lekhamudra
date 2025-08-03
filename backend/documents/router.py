from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
from models import Document
from database import documents_db
from auth.security import get_current_user

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/", response_model=List[Document])
def list_docs(current_user: dict = Depends(get_current_user)):
    return [doc for doc in documents_db.values() if doc.owner == current_user["email"]]


@router.post("/", response_model=Document)
def create_doc(doc: Document, current_user: dict = Depends(get_current_user)):
    doc_id = len(documents_db) + 1
    new_doc = Document(
        id=doc_id,
        title=doc.title,
        content=doc.content,
        owner=current_user["email"],
        last_modified=datetime.utcnow().isoformat()
    )
    documents_db[doc_id] = new_doc
    return new_doc


@router.get("/{doc_id}", response_model=Document)
def get_doc(doc_id: int, current_user: dict = Depends(get_current_user)):
    doc = documents_db.get(doc_id)
    if not doc or doc.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    return doc


@router.put("/{doc_id}", response_model=Document)
def update_doc(doc_id: int, doc: Document, current_user: dict = Depends(get_current_user)):
    existing = documents_db.get(doc_id)
    if not existing or existing.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    updated = doc.copy(update={"last_modified": datetime.utcnow().isoformat()})
    documents_db[doc_id] = updated
    return updated


@router.delete("/{doc_id}")
def delete_doc(doc_id: int, current_user: dict = Depends(get_current_user)):
    doc = documents_db.get(doc_id)
    if not doc or doc.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    del documents_db[doc_id]
    return {"ok": True}
