# Lekhamudra Backend (FastAPI)

## Setup with uv

1. **Install [uv](https://github.com/astral-sh/uv):**

   ```bash
   pip install uv
   ```

2. **Create a virtual environment:**

   ```bash
   uv venv .venv
   ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   uv pip install -r requirements.txt
   ```

5. **Run the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at http://localhost:8000

---

## Endpoints

- `/auth/signup` — Register
- `/auth/login` — Login (OAuth2)
- `/auth/me` — Get current user
- `/documents` — CRUD for documents
- `/documents/{id}/star` — Star a document
- `/documents/{id}/unstar` — Unstar a document
- `/documents/{id}/share` — Get share link

---

## Notes

- Data is stored in memory (resets on server restart).
- CORS is enabled for `http://localhost:3000` (the Next.js frontend).
- You can switch to a real database later with minimal changes.
