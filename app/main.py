# """
# FastAPI application entrypoint.
# """

# from fastapi import FastAPI
# from app.api import router


# app = FastAPI(
#     title="ElCinema Metadata Service",
#     description="Production-ready metadata API for IPTV servers",
#     version="2.0.0"
# )

# # Include router with version prefix
# app.include_router(router, prefix="/v1")

from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="ElCinema Metadata API",
    version="1.0.0",
    description="IPTV-ready API fetching ElCinema work metadata"
)

app.include_router(router)
