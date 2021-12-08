import logging

import uvicorn
from api.v1 import ugc_loader
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import LOGGING

app = FastAPI(
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    title="Post-only API UGC для онлайн-кинотеатра",
    description="Сбор различной аналитики",
    version="1.0.0",
)
app.include_router(ugc_loader.router, prefix="/api/v1/film", tags=["UGC Loader"])
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
