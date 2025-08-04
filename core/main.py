from fastapi import FastAPI
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="Simple Todo App Api",
    description="this is a simple blog app with minimal usage of authentication and post managing",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Mehrdad Motaghian",
        "url": "https://imehrdad.ir/",
        "email": "motaghian@outlook.com",
    },
    license_info={"name": "MIT"},
    docs_url="/swagger",
)