"""from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

# import secrets  # For sharing features


class User(BaseModel):
    email: str
    full_name: Optional[str] = None
    hashed_password: str


class UserIn(BaseModel):
    email: str
    full_name: Optional[str] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Document(BaseModel):
    id: int
    title: str
    content: str = ""
    owner: str
    last_modified: str = ""
    # shared_with: List[str] = []  # Uncomment for sharing
    # public_token: Optional[str] = None  # Uncomment for sharing


# --- In-memory storage ---
users_db = {}
documents_db = {}


SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(email: str):
    return users_db.get(email)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email or email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return users_db[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")



auth_router = APIRouter(prefix="/auth", tags=["auth"])
doc_router = APIRouter(prefix="/documents", tags=["documents"])



@auth_router.post("/signup", response_model=Token)
def signup(user: UserIn):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": get_password_hash(user.password),
    }
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form.username)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}



@doc_router.get("/", response_model=List[Document])
def list_docs(current_user: dict = Depends(get_current_user)):
    return [doc for doc in documents_db.values() if doc.owner == current_user["email"]]


@doc_router.post("/", response_model=Document)
def create_doc(doc: Document, current_user: dict = Depends(get_current_user)):
    doc_id = len(documents_db) + 1
    new_doc = Document(
        id=doc_id,
        title=doc.title,
        content=doc.content,
        owner=current_user["email"],
        last_modified=datetime.utcnow().isoformat(),
        # shared_with=[],  # Uncomment for sharing
        # public_token=None  # Uncomment for sharing
    )
    documents_db[doc_id] = new_doc
    return new_doc


@doc_router.get("/{doc_id}", response_model=Document)
def get_doc(doc_id: int, current_user: dict = Depends(get_current_user)):
    doc = documents_db.get(doc_id)
    if not doc or doc.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    return doc


@doc_router.put("/{doc_id}", response_model=Document)
def update_doc(
    doc_id: int, doc: Document, current_user: dict = Depends(get_current_user)
):
    existing = documents_db.get(doc_id)
    if not existing or existing.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    updated = doc.copy(update={"last_modified": datetime.utcnow().isoformat()})
    documents_db[doc_id] = updated
    return updated


@doc_router.delete("/{doc_id}")
def delete_doc(doc_id: int, current_user: dict = Depends(get_current_user)):
    doc = documents_db.get(doc_id)
    if not doc or doc.owner != current_user["email"]:
        raise HTTPException(status_code=404, detail="Not found or no access")
    del documents_db[doc_id]
    return {"ok": True}


# --- Sharing endpoints ---
# import secrets
# @doc_router.post("/{doc_id}/share-with")
# def share_with(doc_id: int, email: str, current_user: dict = Depends(get_current_user)):
#     doc = documents_db.get(doc_id)
#     if not doc or doc.owner != current_user["email"]:
#         raise HTTPException(status_code=404, detail="Not found or no access")
#     if email not in users_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     if email not in doc.shared_with:
#         doc.shared_with.append(email)
#     return {"ok": True, "shared_with": doc.shared_with}
#
# @doc_router.post("/{doc_id}/share")
# def public_share(doc_id: int, current_user: dict = Depends(get_current_user)):
#     doc = documents_db.get(doc_id)
#     if not doc or doc.owner != current_user["email"]:
#         raise HTTPException(status_code=404, detail="Not found or no access")
#     if not doc.public_token:
#         doc.public_token = secrets.token_urlsafe(12)
#     return {"share_link": f"http://localhost:8000/share/{doc.public_token}"}
#
# @app.get("/share/{token}", response_model=Document)
# def get_by_token(token: str):
#     for doc in documents_db.values():
#         if doc.public_token == token:
#             return doc
#     raise HTTPException(status_code=404, detail="Invalid or expired share link")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(doc_router)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.router import router as auth_router
from documents.router import router as doc_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(doc_router)
