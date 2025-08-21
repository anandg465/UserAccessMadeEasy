# User Access Management Backend

This is the backend for the User Access Management application, built with FastAPI and PostgreSQL.

## Setup

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file (see below).
4. Run the development server:
   ```sh
   uvicorn app.main:app --reload
   ```

## Environment Variables
Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_jwt_secret_key
ORACLE_API_BASE_URL=https://your-oracle-api-base-url
```

## Project Structure
- `app/` - Main application code (to be created)
- `requirements.txt` - Python dependencies
- `README.md` - This file

--- 