from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from django.core.cache import cache
from datetime import datetime, timedelta
import time
import json

from module import admin_config, error

from db.models import (
    TBLBridge
)


# Create your views here.
@api_view(['GET'])
def process_api(request, param1, param2):
    try:
        bridge = TBLBridge.objects.get(dst_address__icontains=request.path, is_active=True)
    except:
        time.sleep(admin_config.DELAY_FOR_BAD_REQUEST)
        return JsonResponse({
            'status_code': status.HTTP_400_BAD_REQUEST,
            'text': error.INVALID_URL
        }, status=status.HTTP_400_BAD_REQUEST)

    rate_limit_id = f'{admin_config.RATE_LIMIT_REDIS_CACHE_PREFIX}_{bridge.id}'
    if rate_limit_id in cache:
        data = cache.get(rate_limit_id)
        for d in data:
            if d < datetime.now() - timedelta(minutes=1):
                data.remove(d)

        rate_limit_per_url = json.loads(bridge.user.permission)['rate_limit_per_url']

        if len(data) < rate_limit_per_url:
            data.append(datetime.now())
            cache.set(rate_limit_id, data, timeout=60)
        else:
            return JsonResponse({
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'text': f'{error.RATE_LIMIT_PER_URL_EXCEED} - {rate_limit_per_url}'
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        cache.set(rate_limit_id, [datetime.now()], timeout=60)

    redis_cache_id = f'{admin_config.BRIDGE_REDIS_CACHE_PREFIX}_{bridge.id}'
    if redis_cache_id in cache:
        data = cache.get(redis_cache_id)
        if bridge.type == 7:    # File to API
            cache.set(redis_cache_id, [])
    else:
        data = []

    bridge.api_calls += 1
    bridge.save()

    if bridge.type == 7:    # File to API
        return JsonResponse({
            'content': data
        }, status=status.HTTP_200_OK)
    else:
        return JsonResponse({
            'frequency (s)': bridge.frequency,
            'content': data
        }, status=status.HTTP_200_OK)
