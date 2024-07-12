Step 1: Set Up Your Environment

Step 2: Install Required Packages

pip install streamlit fastapi uvicorn sqlalchemy openai requests

Step 3:

python populate_db.py

Step 4: Run the FastAPI Backend

uvicorn backend:app --reload


Step 5: Run the Streamlit Frontend

streamlit run frontend.py
