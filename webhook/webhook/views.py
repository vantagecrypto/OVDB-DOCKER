from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
import time
import os
import requests

from module import admin_config, error

from db.models import (
    TBLBridge
)


@api_view(['POST'])
def process_webhook(request, param1, param2):
    try:
        bridge = TBLBridge.objects.get(src_address__icontains=request.path, is_active=True)
    except:
        time.sleep(admin_config.DELAY_FOR_BAD_REQUEST)
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'text': error.INVALID_URL
        }, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(request.body, bytes):
        message = request.body.decode()
    elif isinstance(request.body, str):
        message = request.body
    else:
        message = str(request.body)

    # admin_config.BRIDGE_HANDLE.send_message(bridge.id, message)

    res = requests.post(f'http://{admin_config.OV_APP_HOST_URL}/event/notify_event', json={
        'type': 'on_message',
        'bridge_id': bridge.id,
        'data': {
            'message': message
        }
    })

    return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
