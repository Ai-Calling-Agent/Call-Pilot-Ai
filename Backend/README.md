## How To Start Backend Server

1. cd Backend [if not]
2. python -m venv venv [if not created]
3. .\venv\Scripts\activate [this will activate virtual env]
4. pip install -r requirements.txt
5. python -m uvicorn index:app --reload
