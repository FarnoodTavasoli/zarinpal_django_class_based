from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from zarinpal import ZarinPal
from django.shortcuts import redirect

# It's BEST practice to have your merchant_code within your .env and include it either through your main app's settings or directly here
# DO NOT PUT YOUR merchant_code DIRECTLY WITHIN THE VIEW

# BASE_URL is your website's domain name, i rather include it in my .env to ease the transition from local development to hosted production

class Testcheck(APIView):

    # depending on your payment logic, the checkout can be AllowAny or IsAuthenticated
    # however your verify method must be AllowAny to allow callbacks from zarinpal 
    # permission_classes = [AllowAny]

    def post(self, request):

        pay = ZarinPal(merchant=settings.ZARINPAL_MERCHANT_ID,call_back_url=f'{settings.BASE_URL}/testverify/')
        
        response = pay.send_request(amount=int(1000), description='توضیحات مربوط به پرداخت',mobile='0913*******')

        if response.get('error_code') is None:
            return Response({'redirect_url': response['payment_url']})
        else:
            return Response(f'Error code: {response.get("error_code")}, Error Message: {response.get("message")}', status=status.HTTP_400_BAD_REQUEST)

class Testverify(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        
        pay = ZarinPal(merchant=settings.ZARINPAL_MERCHANT_ID, call_back_url=f"{settings.BASE_URL}/testverify/")
        
        response = pay.verify(request=request, amount=int(1000))
        
        
        if response.get("transaction"):
            if response.get("pay"):
                return redirect(f"{settings.BASE_URL}/Payment?Status=success&RefId={response.get('RefID')}")
            else:
                return redirect(f"{settings.BASE_URL}/Payment?Status=failed")
        else:
            if response.get("status") == "cancel":
                return redirect(f"{settings.BASE_URL}/Payment?Status=cancelled")
            else:
                return redirect(f"{settings.BASE_URL}/Payment?Status=failed")
