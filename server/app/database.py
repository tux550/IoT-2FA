from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import dotenv
import urllib

dotenv.load_dotenv()

PGHOST=os.getenv("PGHOST")
PGUSER=os.getenv("PGUSER")
PGPORT=os.getenv("PGPORT")
PGDATABASE=os.getenv("PGDATABASE")
PGPASSWORD=os.getenv("PGPASSWORD")

encoded_password = urllib.parse.quote_plus(PGPASSWORD)

SQLALCHEMY_DATABASE_URL = f"postgresql://{PGUSER}:{encoded_password}@{PGHOST}:{PGPORT}/{PGDATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
