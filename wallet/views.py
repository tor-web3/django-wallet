from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.http import Http404, JsonResponse
from django.views.generic.list import BaseListView, View
from django.utils import timezone
from wallet.models import Address
from django.core import serializers
import json

class AddressActiveView(View):

    def get(self, request, address, *args, **kwargs):
        try:
            from wallet.chainstate.models import State
            state_obj = State.objects.get(
                address__address=address
            )
            state_obj.is_update = True
            state_obj.flush()

            return JsonResponse({
                "results": "success"
            })
        except State.DoesNotExist as e:
            return JsonResponse({
                "error": e.args
            })


class AddressListView(View):

    def get(self, request, *args, **kwargs):
        try:
            created_time = request.GET.get("created_time",0)
            timestamp = int(created_time)
            created_at = timezone.datetime.utcfromtimestamp(timestamp)

            address_obj_list = Address.objects.filter(
                created_at__gte=created_at
            )[:10000]
            data = serializers.serialize("json", address_obj_list)
            return JsonResponse({
                "results": json.loads(data)
            })
        except Exception as e:
            return JsonResponse({
                "error": e.args
            })
