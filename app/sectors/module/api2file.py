import _thread as thread
import time
from datetime import datetime
import requests
import json

from . import log, file

from sectors.common import admin_config

from db.models import (
    TBLBridge
)


class Bridge:
    """
    API to File Data Bridge
    """

    def __init__(self, bridge_info):
        self.bridge_info = bridge_info

        self.connection_status = None
        self.connection_text = 'Waiting for connect'
        self.log = log.BridgeLog(bridge_info)
        self.cache = self.log.get_last_log()

        self.file = file.File(bridge_info['dst_address'], bridge_info['format'])

        # self.REDIS_CACHE_ID = f"{admin_config.BRIDGE_REDIS_CACHE_PREFIX}_{self.bridge_info['id']}"
        self.REDIS_CACHE_TTL = self.bridge_info['frequency']

    def run_api(self):
        count = 0
        while True:
            if not self.connection_status:
                break

            if count == 0 or count >= self.REDIS_CACHE_TTL:
                count = 0
                try:
                    self.add_cache(f"API:Call - {self.bridge_info['src_address']}")
                    res = requests.get(self.bridge_info['src_address'], verify=False)
                    try:
                        # cache.set(self.REDIS_CACHE_ID, res.json(), timeout=self.REDIS_CACHE_TTL)
                        self.add_cache(f'API:Receive - {res.text}')
                        self.write_file(res.text)
                    except Exception as e:
                        self.add_cache(f'FILE:Update - Exception - {e}')
                except Exception as e:
                    self.add_cache(f'API:Call - Exception - {e}')

            time.sleep(1)
            count += 1

    def open(self):
        self.connection_status = True
        self.connection_text = 'API:Open - Ready'
        thread.start_new_thread(self.run_api, ())
        self.add_cache(self.connection_text)

    def close_log(self):
        self.log.close()

    def close(self):
        self.connection_status = False
        self.connection_text = f'API:Closed'
        self.add_cache(self.connection_text)

    def is_connected(self):
        while self.connection_status is None:
            time.sleep(0.1)

        return self.connection_status

    def write_file(self, data):
        self.add_cache(f'FILE:Update - {data}')
        self.file.truncate()
        self.file.write(data)

        bridge = TBLBridge.objects.get(id=self.bridge_info['id'])
        bridge.api_calls += 1
        bridge.save()

    def add_cache(self, data):
        self.trace(data)

        if len(self.cache) > admin_config.LOCAL_CACHE_LIMIT:
            self.cache.pop(0)

        cache_data = {
            'date': datetime.utcnow().strftime('%m/%d/%Y, %H:%M:%S'),
            'data': data
        }
        self.cache.append(cache_data)

        self.log.write_log(json.dumps(cache_data))

    def get_cache(self):
        return self.cache

    def trace(self, trace_log):
        if admin_config.TRACE_MODE:
            print(f"{datetime.utcnow()}: {self.bridge_info['name']}_{self.bridge_info['user_id']}: {trace_log}")
