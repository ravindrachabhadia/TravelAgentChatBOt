# populate_db.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend import Base, Package

DATABASE_URL = "sqlite:///./travel_agent.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear existing data
db.query(Package).delete()

sample_packages = [
    {"origin": "Mumbai", "destination": "London", "price": 500.0, "details": "Direct flight, 7 days stay, breakfast included"},
    {"origin": "Hong Kong", "destination": "London", "price": 600.0, "details": "One stopover, 5 days stay, all meals included"},
    {"origin": "New York", "destination": "Paris", "price": 700.0, "details": "Direct flight, 10 days stay, breakfast included"},
    {"origin": "Sydney", "destination": "Tokyo", "price": 800.0, "details": "Direct flight, 5 days stay, breakfast and dinner included"},
]

for pkg in sample_packages:
    package = Package(**pkg)
    db.add(package)
db.commit()
db.close()
