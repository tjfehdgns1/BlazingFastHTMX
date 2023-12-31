from typing import Optional

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import mockup_models
from .mockup_database import SessionLocal, engine

mockup_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    num_films = db.query(mockup_models.Film).count()

    if num_films == 0:
        films = [
            {"name": "Baldur's", "year": "2023", "rating": "10"},
            {"name": "goty", "year": "2000", "rating": "9"},
            {"name": "daram", "year": "2021", "rating": "8"},
        ]
        for film in films:
            db.add(mockup_models.Film(**film))
        db.commit()

    else:
        print(f"{num_films} films in database")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root():
    return {"message": "Welcome"}


@app.get("/index/", response_class=HTMLResponse)
async def read_index(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    page: int = 1,
):
    N = 2
    OFFSET = (page - 1) * N
    films = db.query(mockup_models.Film).offset(OFFSET).limit(N)
    print(films)
    context = {"request": request, "films": films, "page": page}

    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)
