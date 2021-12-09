from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException
from models.request import RequestForUGS

from services.kafka_loader import kafka_loader

router = APIRouter()


def create_answer(*, was_loaded: bool, movie_id: UUID, user_id: UUID) -> dict:
    return {
        "result": {
            "was_loaded": was_loaded,
            "movie_id": str(movie_id),
            "user_id": str(user_id),
        }
    }


@router.post("/load_inner", summary="UGC Loader inner ednpoint", status_code=201)
def load_innerdata_to_kafka(request_for_ugs: RequestForUGS):
    print(request_for_ugs)
    was_loaded: bool = kafka_loader.load(request_for_ugs)
    result = create_answer(
        was_loaded=was_loaded,
        movie_id=request_for_ugs.payload.movie_id,
        user_id=request_for_ugs.payload.user_id,
    )
    if was_loaded:
        return result
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=result)


@router.post("/load_outer", summary="UGC Loader outer ednpoint", status_code=201)
def load_innerdata_to_kafka(request_for_ugs: RequestForUGS):
    # TODO parse jwt
    kafka_loader.load(request_for_ugs)
