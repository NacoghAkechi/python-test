from django.urls import path

from gas.web.views import create_bill

urlpatterns = [path("api/bills/", create_bill)]
