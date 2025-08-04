from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routers

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