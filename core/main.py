from fastapi import FastAPI,Depends,Response,Request,BackgroundTasks,Request
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routers
from users.routes import router as users_routers
from users.models import UserModel
import time
import random
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time




tags_metadata = [
    {
        "name": "tasks",
        "description": "Operations related to task management",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https://example.com/docs/tasks"
        }
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(
    title="Todo Application",
    description="this is a section for description",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mehrdad Motaghian",
        "url": "http://imehrdad.ir/",
        "email": "motaghian@outlook.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
    openapi_tags=tags_metadata
)

app.include_router(tasks_routers) # ,prefix="/api/v1"
app.include_router(users_routers)

from auth.jwt_auth import get_authenticated_user

@app.get("/private_token_jwt")
def private_route(user = Depends(get_authenticated_user)):
    print(user.id)
    return {"message":"this is a private route"}

@app.get("/public")
def public_route():
    return {"message":"this is a public route"}

# from auth.token_auth import get_authenticated_user

# @app.get("/private_token")
# def private_route(user = Depends(get_authenticated_user)):
#     print(user.username)
#     return {"message":"this is a private route"}

##########################

# from auth.basic_auth import get_authenticated_user

# @app.get("/public")
# def public_route():
#     return {"message":"this is a public route"}

# @app.get("/private")
# def private_route(user: UserModel = Depends(get_authenticated_user)):
#     print(user)
#     return {"message":"this is a private route"}



@app.post("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="test", value="fake-cookie-session-value")
    return {"message": "cookies set"}

@app.get("/get-cookie")
def get_cookie(request: Request):
    print(request.cookies)
    return {"message": "cookies set"}


# background task handling

def start_task(task_id):
    print(f"doing the process: {task_id}")
    time.sleep(random.randint(3,10))
    print(f"finished task {task_id}")


@app.get("/initiate-task", status_code=200)
async def initiate_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(start_task,task_id=random.randint(1,100))
    return JSONResponse(content={"detail":"task is done"})

@app.get("/is_ready", status_code=200)
async def readiness():
    return JSONResponse(content="ok")



from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
import httpx


cache_backend = InMemoryBackend()
FastAPICache.init(cache_backend)

async def request_current_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        current_weather = data.get("current", {})
        return current_weather
    else:
        return None
    
@app.get("/fetch-current-weather", status_code=200)
@cache(expire=10)
async def fetch_current_weather(latitude: float = 40.7128, longitude: float = -74.0060):
    current_weather = await request_current_weather(latitude, longitude)

    if current_weather:
        return JSONResponse(content={"current_weather": current_weather})
    else:
        return JSONResponse(content={"detail": "Failed to fetch weather"}, status_code=500)
    
    
    
# A list of specific origins that are allowed to make cross-origin requests.
origins = {
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",  # docs/sample login
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],   # Allows all methods
    allow_headers=["*"],   # Allows all headers
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response