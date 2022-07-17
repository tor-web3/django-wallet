from django.views import View
from django.http import JsonResponse
from wallet.history.models import Deposit

import logging
logger = logging.getLogger(__name__)


class AddressDepositView(View):

    def post(self, request, *args, **kwargs):
        try:
            print(request.POST)
            # TODO: 参数解析
            # deposit_obj = Deposit()
            # deposit_obj.txid =
            # deposit_obj.counterparty_address =
            # deposit_obj.deposit_address =
            # deposit_obj.amount =
            # deposit_obj.token =
            # deposit_obj.memo =
            # deposit_obj.status =
            # deposit_obj.error_info =
            # deposit_obj.finished_time =
            # deposit_obj.block_time =
            return JsonResponse({
                "results":"success"
            })
        except Exception as e:
            from django.core import serializers
            deposit_obj = Deposit.objects.first()
            data = {"eg":"eg"}
            if deposit_obj :
                data = serializers.serialize("json", deposit_obj)
            return JsonResponse({
                "results": e.args,
                "eg":
                    data
                
            })
