import requests
import json

SANDBOX = False # set to True for testing purposes
# also for sandbox mode use any random UUID-V4 for your merchant_code

# import uuid
# merchant = uuid.uuid4()

if SANDBOX:
    subdom = "sandbox"
    paysub = 'sandbox'
else:
    subdom = "payment"
    paysub = 'www'

class ZarinPal:
    ZP_API_REQUEST = f"https://{subdom}.zarinpal.com/pg/v4/payment/request.json"
    ZP_API_VERIFY = f"https://{subdom}.zarinpal.com/pg/v4/payment/verify.json"
    ZP_API_STARTPAY = f"https://{paysub}.zarinpal.com/pg/StartPay/"+"{authority}"

    def __init__(self, merchant, call_back_url):
        self.MERCHANT = merchant
        self.callbackURL = call_back_url

    def send_request(self, amount, description, email=None, mobile=None):

        metadata = {}
        if mobile:
            metadata["mobile"] = mobile
        if email:
            metadata["email"] = email

        req_data = {
            "merchant_id": self.MERCHANT,
            "amount": amount,
            "callback_url": self.callbackURL,
            "description": description,
            "metadata": metadata,
        }
        req_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        try:
            response = requests.post(self.ZP_API_REQUEST, json=req_data, headers=req_header)
            if response.status_code != 200:
                return {"error": "Zarinpal unreachable", "status_code": response.status_code}

            data = response.json()

            if data.get("data", {}).get("code") == 100:
                authority = data["data"]["authority"]
                return {
                    "status": "pending",
                    "authority": authority,
                    "payment_url": self.ZP_API_STARTPAY.format(authority=authority)
                }
            else:
                errors = data.get("errors", {})
                return {
                    "status": "error",
                    "message": errors.get("message"),
                    "code": errors.get("code")
                }

        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "exception"}

    def verify(self, request, amount):
        t_status = request.query_params.get('Status')
        t_authority = request.query_params.get('Authority')

        if t_status == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json"}
            req_data = {
                "merchant_id": self.MERCHANT,
                "amount": amount,
                "authority": t_authority
            }
            req = requests.post(url=self.ZP_API_VERIFY, json=req_data, headers=req_header)
            data = req.json()

            if not data.get("errors"):
                t_status = data['data']['code']
                if t_status == 100:
                    # paid successfully 
                    return {"transaction": True, "pay": True, "RefID": data['data']['ref_id'], "message": None}

                elif t_status == 101:
                    # payment was previously paid and was reverified
                    return {"transaction": True, "pay": False, "RefID": None, "message": data['data']['message']}

                else:
                    # peyment process failed/cancelled
                    return {"transaction": False, "pay": False, "RefID": None, "message": data['data']['message']}

            else:
                errors = data.get("errors", {})
                e_code = errors.get("code")
                e_message = errors.get("message", "zarinpal returned unhandled error")

                return {"status": 'ok', "message": e_message, "error_code": e_code}
        else:
            return {"status": 'cancel', "message": 'transaction failed or canceled by user'}
