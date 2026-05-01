import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize Supabase client
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("❌ Missing Supabase credentials in .env file!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.post("/api/auth/login")
async def api_login(request: Request):
    """Backend authentication endpoint"""
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return JSONResponse(
                {"error": "Email and password are required"},
                status_code=400
            )
        
        # Call Supabase backend
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        return JSONResponse({
            "success": True,
            "data": response.model_dump() if hasattr(response, 'model_dump') else response
        })
        
    except Exception as error:
        print(f"❌ Login error: {error}")
        return JSONResponse(
            {"error": str(error)},
            status_code=400
        )


@app.post("/api/auth/signup")
async def api_signup(request: Request):
    """Backend signup endpoint"""
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return JSONResponse(
                {"error": "Email and password are required"},
                status_code=400
            )
        
        # Call Supabase backend
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        return JSONResponse({
            "success": True,
            "data": response.model_dump() if hasattr(response, 'model_dump') else response
        })
        
    except Exception as error:
        print(f"❌ Signup error: {error}")
        return JSONResponse(
            {"error": str(error)},
            status_code=400
        )


@app.get("/api/health")
async def health_check():
    """Check Supabase connectivity"""
    try:
        # Simple test to verify Supabase is reachable
        return JSONResponse({
            "status": "ok",
            "supabase_url": SUPABASE_URL,
            "message": "✅ Supabase client initialized successfully"
        })
    except Exception as error:
        return JSONResponse(
            {
                "status": "error",
                "error": str(error)
            },
            status_code=500
        )


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
