from wallet import views
from django.urls import path

urlpatterns = [
    path('address/<address>/',views.AddressActiveView.as_view(),name='wallet-address-active',),
    path('address/',views.AddressListView.as_view())
]
