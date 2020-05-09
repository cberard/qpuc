from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_database/sql.db"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


DATABASE_URL = "postgres://nelwwypmwkrfpr:7e46d04aff68ed86c28e64a6f296127a6925e981b15f7333d28f3a84fc9943f3@ec2-54-217-236-206.eu-west-1.compute.amazonaws.com:5432/d4kf4q680s66e3"

engine = create_engine(
    DATABASE_URL#, connect_args={"check_same_thread": False}
)

#SQLALCHEMY_DATABASE_URL = "sqlite:///qpuc_app/sql_database/sql.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


#engine = create_engine(
#    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
#)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()