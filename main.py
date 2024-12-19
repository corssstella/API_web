from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

class Cake(BaseModel):
    id: int
    name: str
    description: str
    price: float

class Service(BaseModel):
    id: int
    name: str
    description: str

class Contact(BaseModel):
    address: str
    phone: str
    email: str

CAKES_DB = [
    Cake(id=1, name="Шоколадный торт", description="Нежный шоколадный торт с кремом.", price=1500.0),
    Cake(id=2, name="Тирамису", description="Классический итальянский десерт с кофе и маскарпоне.", price=1200.0),
    Cake(id=3, name="Чизкейк", description="Разнообразные чизкейки с различными начинками.", price=1300.0),
    Cake(id=4, name="Фруктовый торт", description="Легкий и свежий торт с фруктами.", price=1400.0),
    Cake(id=5, name="Медовик", description="Традиционный медовый торт с кремом.", price=1100.0),
]

SERVICES_DB = [
    Service(id=1, name="Доставка", description="Доставка тортов прямо к вашему дому или офису."),
    Service(id=2, name="Индивидуальный заказ", description="Возможность заказать торт по вашему вкусу и дизайну."),
    Service(id=3, name="Праздничное оформление", description="Оформление тортов для праздников и особых случаев."),
]

CONTACT_DB = Contact(
    address="ул. Университетская 31, г. Сургут",
    phone="+7 (954) 356-5555",
    email="bestcake222@gmail.com"
)

app = FastAPI()

@app.get("/cakes/")
def read_cakes():
    return CAKES_DB

@app.get("/cakes/{id}")
def read_cake(id: int):
    for cake in CAKES_DB:
        if cake.id == id:
            return cake
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.post("/cakes/")
def create_cake(cake: Cake):
    for existing_cake in CAKES_DB:
        if existing_cake.id == cake.id:
            raise HTTPException(status_code=400, detail="Торт с таким ID уже существует")
    CAKES_DB.append(cake)
    return cake

@app.delete("/cakes/{id}")
def delete_cake(id: int):
    for cake in CAKES_DB:
        if cake.id == id:
            CAKES_DB.remove(cake)
            return {"detail": "Торт успешно удален"}
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.get("/services/")
def read_services():
    return SERVICES_DB

@app.get("/services/{id}")
def read_service(id: int):
    for service in SERVICES_DB:
        if service.id == id:
            return service
    raise HTTPException(status_code=404, detail="Услуга не найдена")

@app.get("/contact/")
def read_contact():
    return CONTACT_DB

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)