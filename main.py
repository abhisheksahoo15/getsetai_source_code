import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "supabase_url": os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        "supabase_key": os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "supabase_url": os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        "supabase_key": os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    })

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {
        "request": request,
        "supabase_url": os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        "supabase_key": os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    })
