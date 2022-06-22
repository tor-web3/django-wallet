from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.http import Http404, JsonResponse
from django.views.generic.list import BaseListView,View


class AddressActiveView(View):
    """Handle AutocompleteWidget's AJAX requests for data."""

    def get(self, request, *args, **kwargs):

        
        return JsonResponse({
            'results': [
            ],
        })
