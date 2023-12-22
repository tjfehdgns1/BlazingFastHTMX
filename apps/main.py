from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")


@app.get("/index/", response_class=HTMLResponse)
async def read_root(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    films = db.query(models.Film).all()
    print(films)
    context = {"request": request, "films": films}

    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)
