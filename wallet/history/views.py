from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


import logging
logger = logging.getLogger(__name__)


class AddressDepositView(View):

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            print(request.POST)
            return JsonResponse({
                "results":"success"
            })
        except Exception as e:
            return JsonResponse({
                "results": e.args
            })
