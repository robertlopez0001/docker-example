from fastapi import FastAPI, Request
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import settings
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

class Bond(SQLModel, table=True):
    parse_key : str = Field(index=True, primary_key=True)
    maturity_date : str = Field()
    ask_price : int | None = Field(default=None)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Load templates from the "templates" folder
templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/hello/")
def hello():
    return "Hello, Docker! From Robert Lopez!"


@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


@app.post("/bonds/")
def create_bond(bond : Bond):
    with Session(engine) as session:
        session.add(bond)
        session.commit()
        session.refresh(bond)
        return bond



@app.get("/bonds/")
def read_bonds():
    with Session(engine) as session:
        query = select(Bond)
        query = query.where(Bond.ask_price > 90)
        bonds = session.exec(query).all()
        return bonds