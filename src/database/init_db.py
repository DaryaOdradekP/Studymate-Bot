from src.database.db import Base, engine
from src.database.models import Subject


def init_db():
    Base.metadata.create_all(bind=engine)
    