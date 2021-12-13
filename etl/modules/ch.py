from clickhouse_driver import Client
from etl.config import (CH_HOST, CH_TABLE)


class ETLClickhouseDriver:
    def __init__(self):
        self.host = CH_HOST
        self.table = CH_TABLE

    def get_ch(self):
        return Client.from_url(self.host)
