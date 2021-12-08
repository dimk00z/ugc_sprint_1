from fastapi import APIRouter
from models.request import RequestForUGS

from services.kafka_loader import kafka_loader

router = APIRouter()


@router.post("/", summary="UGC Loader inner ednpoint")
def load_innerdata_to_kafka(request_for_ugs: RequestForUGS):
    kafka_loader.load(request_for_ugs)


@router.post("/load_outer", summary="UGC Loader outer ednpoint")
def load_innerdata_to_kafka(request_for_ugs: RequestForUGS):
    # TODO parse jwt
    kafka_loader.load(request_for_ugs)
