from wallet.history import views
from django.urls import path,include

urlpatterns = [
    path('deposit/',views.AddressDepositView.as_view()),
]
