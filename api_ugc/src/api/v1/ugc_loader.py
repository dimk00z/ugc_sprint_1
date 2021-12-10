import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query
from models.request import RequestForUGS, create_random_request

from services.ugc_kafka_producer import ugc_kafka_producer

router = APIRouter()
logger = logging.getLogger(__name__)


def create_answer(*, was_loaded: bool, movie_id: UUID, user_id: UUID) -> dict:
    return {
        "result": {
            "was_loaded": was_loaded,
            "movie_id": str(movie_id),
            "user_id": str(user_id),
        }
    }


@router.post("/produce", summary="UGC produce endpoint", status_code=201)
async def inner_produce(request_for_ugs: RequestForUGS):
    logger.debug(request_for_ugs)
    was_produced: bool = await ugc_kafka_producer.produce(request_for_ugs=request_for_ugs)
    result = create_answer(
        was_loaded=was_produced,
        movie_id=request_for_ugs.payload.movie_id,
        user_id=request_for_ugs.payload.user_id,
    )
    if was_produced:
        return result
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result)


@router.post("/batch_produce", summary="UGC batch produce endpoint", status_code=201)
async def batch_inner(requests_for_ugs: list[RequestForUGS]):
    logger.debug(requests_for_ugs)
    was_produced: bool = await ugc_kafka_producer.batch_produce(requests=requests_for_ugs)
    result = {"batch_produced": was_produced}
    if was_produced:
        return result
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result)


# WARNING only for debug
@router.post("/random_batch_produce", summary="UGC produce inner endpoint", status_code=201)
async def random_batch_produce(batch_count: int = Query(default=500, alias="batch_count")):
    batch = [create_random_request() for _ in range(batch_count)]
    print(len(batch))
    was_produced: bool = await ugc_kafka_producer.batch_produce(requests=batch)
    result = {"batch_produced": was_produced}
    if was_produced:
        return result
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result)
