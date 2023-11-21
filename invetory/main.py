from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_om import get_redis_connection,HashModel

from pydantic import BaseModel



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-12052.c52.us-east-1-4.ec2.cloud.redislabs.com",
    port=12052,
    password="sWgL3JktX6hcErNcr4PPRnsDedxNRMeP",
    decode_responses=True,
)

class Product(HashModel):
    id: str | None = None
    name: str | None = None
    price: float
    quantity: int

    class Meta:
        database = redis


class ProductModel(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    return {
            'id': product.pk,
            'name': product.name or "",
            'price': float(product.price),
            'quantity': int(product.quantity)
        }


@app.post('/products', response_model=ProductModel)
def create(product: ProductCreate):
    hash_model = Product(**product.dict())
    hash_model.save()
    return format(hash_model.pk)

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
