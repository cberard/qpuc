from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_database/sql.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

DATABASE_URL = 'postgres://atkwirkivycoqi:59ccfbcf8f2d247871fbc6b66c9e857387ce6dbeaeb6fc5188d1a11c1b0ae549@ec2-46-137-156-205.eu-west-1.compute.amazonaws.com:5432/db5uj8pccpt9dd'

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()