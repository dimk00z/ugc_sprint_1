import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from etl.config import (CH_HOST, CH_TABLE)


class ETLClickhouseDriver:
    def __init__(self):
        self.host = CH_HOST
        self.table = CH_TABLE

    @backoff.on_exception(backoff.expo, Error)
    def get_ch(self):
        return Client.from_url(self.host)
