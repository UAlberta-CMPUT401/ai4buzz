from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ubuntu:ubuntu@2d7a6.yeg.rac.sh/postgres" # TODO: ipv6 psycopg2 docker build error
SQLALCHEMY_DATABASE_URL = "postgresql://ohhykmmy:kC5gr49OfXLn1Kkufk_y1CtHJUAhTPwM@kashin.db.elephantsql.com/ohhykmmy"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
