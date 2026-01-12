from sqlmodel import Session, select
from database import engine
from models import Product


DEFAULT_PRODUCTS = [
    Product(name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(name="Table", description="A wooden table", price=199.99, quantity=20),
]


def init_db():
    with Session(engine) as session:
        if session.exec(select(Product)).first():
            return

        session.add_all(DEFAULT_PRODUCTS)
        session.commit()
