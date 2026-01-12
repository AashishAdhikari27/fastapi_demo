from sqlmodel import SQLModel, create_engine,Session 

database_url = "postgresql://postgres:postgres@localhost/product_db"

engine = create_engine(database_url, echo=True)




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
