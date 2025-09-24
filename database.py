from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:9172ps@localhost:5432/demo_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)