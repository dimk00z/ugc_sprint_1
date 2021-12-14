import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error


class ETLClickhouseDriver:
    def __init__(self, host: str, table: str):
        self.host = host
        self.table = table

    @backoff.on_exception(backoff.expo, Error)
    def get_ch(self):
        return Client.from_url(self.host)
