# backend.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import openai
import logging
import spacy

# Initialize FastAPI
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Database setup
DATABASE_URL = "sqlite:///./travel_agent.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    price = Column(Float)
    details = Column(String)

Base.metadata.create_all(bind=engine)

class QueryRequest(BaseModel):
    query: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.post("/query/")
async def handle_query(request: QueryRequest):
    query = request.query.lower()
    logger.info(f"Received query: {query}")
    try:
        if any(keyword in query for keyword in ["package", "cost", "price", "ticket"]):
            return handle_proprietary_query(query)
        else:
            return handle_general_query(query)
    except Exception as e:
        logger.error(f"Error processing query: {query}, Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def handle_general_query(query: str):
    openai.api_key = " "  # Add your OpenAI API key here
    logger.info(f"Handling general query: {query}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": query}]
        )
        logger.info(f"OpenAI response: {response}")
        return {"response": response.choices[0].message['content'].strip()}
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="Error with OpenAI API")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")

def extract_locations(query: str):
    doc = nlp(query)
    locations = [ent.text.lower() for ent in doc.ents if ent.label_ == "GPE"]
    if len(locations) >= 2:
        return locations[0], locations[1]
    return None, None

def handle_proprietary_query(query: str):
    db = SessionLocal()
    try:
        origin, destination = extract_locations(query)
        if origin and destination:
            packages = db.query(Package).filter(text("lower(origin) = :origin and lower(destination) = :destination")).params(origin=origin, destination=destination).all()
            if packages:
                return {"response": [f"{pkg.origin} to {pkg.destination} costs {pkg.price} and details: {pkg.details}" for pkg in packages]}
            else:
                return {"response": f"No packages found from {origin.capitalize()} to {destination.capitalize()}"}
        else:
            packages = db.query(Package).all()
            return {"response": [f"{pkg.origin} to {pkg.destination} costs {pkg.price} and details: {pkg.details}" for pkg in packages]}
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(status_code=500, detail="Database query error")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
