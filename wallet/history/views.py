from django.views import View
from django.http import JsonResponse


import logging
logger = logging.getLogger(__name__)



class AddressActiveView(View):

    def get(self, request, address, *args, **kwargs):
        try:
            from wallet.chainstate.models import State
            state_obj = State.objects.get(
                    address__address   = address
                )
            state_obj.is_update = True
            state_obj.flush()
                
            return JsonResponse({
                "results":"success"
            })
        except State.DoesNotExist as e:
            return JsonResponse({
                "results": e.args
            })
