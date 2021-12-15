import logging
from http import HTTPStatus

import jwt
from aiocache import Cache, cached
from aiocache.serializers import PickleSerializer
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient, HTTPError
from py_auth_header_parser import parse_auth_header

from core.settings import get_settings

logger = logging.getLogger(__name__)

redis_setting = get_settings().redis_settings


def apply_middleware(app: FastAPI):
    @app.middleware("http")
    async def check_auth(request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header is not None:
            correct_auth = get_auth_answer(
                auth_url=get_settings().app.auth_host, header=auth_header
            )
            if correct_auth:
                return await call_next(request)

        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content={"Error": "Authorization error"},
        )


def parse_header(auth_header) -> tuple:
    parsed_auth_header = parse_auth_header(auth_header)
    jwt_token = parsed_auth_header["access_token"]
    username = None
    roles = None
    try:
        decoded_jwt = jwt.decode(
            jwt_token,
            get_settings().app.jwt_public_key,
            algorithms=[get_settings().app.jwt_algorithm],
        )
        username = decoded_jwt["username"]
        roles = decoded_jwt["roles"]
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as jwt_error:
        logger.exception(jwt_error)
    is_authenticated: bool = username and roles
    return is_authenticated


@cached(
    ttl=redis_setting.ttl,
    cache=Cache.REDIS,
    serializer=PickleSerializer(),
    port=redis_setting.port,
    endpoint=redis_setting.endpoint,
    namespace="main",
    pool_min_size=redis_setting.pool_min_size,
    pool_max_size=redis_setting.pool_max_size,
    noself=True,
)
async def get_auth_answer(auth_url, headers) -> bool:
    is_authenticated: bool = False
    try:
        async with AsyncClient() as client:
            auth_answer = await client.get(auth_url, headers=dict(headers))
            is_authenticated = parse_header(auth_answer.headers)
            logger.info(auth_answer)
    except HTTPError as request_error:
        logger.exception(request_error)
    return is_authenticated
