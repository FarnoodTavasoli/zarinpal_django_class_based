from django.urls import path
from .views import Testcheck, Testverify

urlpatterns = [

    path('testcheck/',Testcheck.as_view(),name='testcheck'),
    path('testverify/',Testverify.as_view(),name='testverify'),
]
