from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templating = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def read_index(request: Request):
    return templating.TemplateResponse("index.html", {"request": request})