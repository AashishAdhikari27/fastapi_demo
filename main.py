import uvicorn
from fastapi import FastAPI, Depends ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Product

from sqlmodel import SQLModel, select , Session
# from database import create_db_and_tables, get_session
from init_db import init_db
from database import create_db_and_tables, get_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def greet():
    return "Hello, World!"

# def get_db():
#     db = get_session()
#     try:
#         yield db
#     finally:
#         db.close()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    init_db()  # REMOVE this line in production




# # list of products with 4 products like phones, laptops, pens, tables
# products = [
#     Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
#     Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
#     Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
#     Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
# ]

@app.get("/products/")
def get_products(session : Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products




# @app.get("/product/{id}")
# def get_product_by_id(id :int):
#     for product in products:
#         if product.id == id:
#             return product
#     return {"error": "Product not found"}



@app.get("/product/{id}")
def get_product_by_id(id: int, session: Session = Depends(get_session)):
    product = session.get(Product, id)
    if product:
        return product
    return {"error": "Product not found"}





# @app.post("/product")
# def add_product(product :Product):
#     products.append(product)

#     return product


@app.post("/products/")
def add_product(product : Product ,session: Session = Depends(get_session)):
                session.add(product)
                session.commit()
                session.refresh(product)
                return product

# @app.put("/product")
# def update_product(product:Product,id:int):
#     for i in range(len(products)):
#         if products[i].id == id:
#             products[i]= product

#             return "product added successfully"
    
#     return "product not found"

@app.put("/products/{id}")
def update_product(id:int , data :Product ,session: Session = Depends(get_session) ):
      product = session.get(Product,id)

      if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
      
      # 2️⃣ Update fields
      product.id = data.id 
      product.name = data.name
      product.description = data.description
      product.price = data.price
      product.quantity = data.quantity

      # 3️⃣ Commit changes
      session.add(product)
      session.commit()
      session.refresh(product)  # optional: refresh to get updated values


      return product

 

      
   

# @app.delete("/product")
# def delete_product(id:int):
#     for i in range(len(products)):
#         if products[i].id == id:
#             # products.pop(i)  ## this also deletes product
#             del products[i]

#             return "product deleted"
        
#     return "product not found !!!!"


@app.delete("/products/{id}")
def delete_product(id:int,session: Session = Depends(get_session)):
      product = session.get(Product,id)

      if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
      
      session.delete(product)
      session.commit()


      return {"message":" product deleted"}



      