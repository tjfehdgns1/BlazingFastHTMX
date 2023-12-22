from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/index/", response_class=HTMLResponse)
async def read_root(request: Request):
    films = [
        {"name": "Star Wars: 2", "year": "2019", "rating": "3"},
        {"name": "Carribian Pirates", "year": "2009", "rating": "8"},
        {"name": "Shit", "year": "1989", "rating": "7"},
    ]
    context = {"request": request, "films": films}
    return templates.TemplateResponse("index.html", context)
