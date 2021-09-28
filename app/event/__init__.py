from sectors.common import admin_config
from sectors.module import bridge, billing
import _thread as thread
import time
import os
from django.contrib.auth import authenticate
import urllib3

from db.models import (
    TBLUser
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run_module():
    time.sleep(5)

    ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@gmail.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'xvX9BCE7RXdMzG4V')

    user = authenticate(username=ADMIN_USER, password=ADMIN_PASSWORD)
    if not user:
        user = TBLUser()
        user.email = ADMIN_EMAIL
        user.username = ADMIN_USER
        user.set_password(ADMIN_PASSWORD)
        user.is_superuser = True
        user.is_active = True
        user.save()

    if admin_config.BRIDGE_HANDLE is None:
        print('Module start...')
        try:
            admin_config.BRIDGE_HANDLE = bridge.BridgeQueue()
            admin_config.BRIDGE_HANDLE.fetch_all_bridges()
            admin_config.BRIDGE_HANDLE.start_all()
        except Exception as e:
            print(f'Module exception...{e}')
    else:
        pass

    if admin_config.BILLING_HANDLE is None:
        print('Billing start...')
        try:
            admin_config.BILLING_HANDLE = billing.Billing()
            admin_config.BILLING_HANDLE.start_conversion_pricing()
        except Exception as e:
            print(f'Billing exception...{e}')
    else:
        pass


thread.start_new_thread(run_module, ())
