from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.http import Http404, JsonResponse
from django.views.generic.list import BaseListView,View


class AddressActiveView(View):
    """Handle AutocompleteWidget's AJAX requests for data."""

    def get(self, request, address, *args, **kwargs):
        try:
            from wallet.chainstate.models import State
            state_obj = State.objects.get(
                    address__address   = address
                )
            state_obj.is_update = True
            state_obj.is_active = True
            state_obj.save()
                
            return JsonResponse({
                "results":"success"
            })
        except State.DoesNotExist as e:
            return JsonResponse({
                "results": e.args
            })
