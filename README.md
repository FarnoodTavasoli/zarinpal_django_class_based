# Django Zarinpal Integration
پیاده‌سازی ساده API درگاه پرداخت زرینپال در رستفریموورک جنگو
A simple Django REST-API integration for the Zarinpal payment gateway.

[فارسی (Persian)](#فارسی) | [English](#english)

---

## <a name="فارسی"></a><img src="https://flagofiran.com/files/Flag_of_Iran_simplified.svg" width="24" alt="Lion and Sun Flag"> راهنمای سریع (فارسی)
### ۱. راه‌اندازی

* **جایگذاری فایل‌ها**: فایل `zarinpal.py` را در پروژه خود قرار دهید. فایل‌های `views.py` و `urls.py` حاوی کدهای نمونه برای استفاده در اپلیکیشن شما هستند.

* **نصب نیازمندی‌ها**: برای یک پروژه جدید، تمام وابستگی‌ها را نصب کنید.
    ```bash
    pip install requests
    pip install djangorestframework
    ```

* **پیکربندی `settings.py`**: مرچنت کد زرین‌پال و آدرس سایت خود را اضافه کنید. استفاده از متغیرهای محیطی (env) به شدت توصیه می‌شود.
    ```python
    # settings.py
    ZARINPAL_MERCHANT_ID = 'YOUR_ZARINPAL_MERCHANT_ID' # مرچنت کد شما
    BASE_URL = 'http://127.0.0.1:8000' # در حالت پروداکشن، دامنه خود را وارد کنید
    ```

* **پیکربندی `urls.py`**:
    ```python
    # your_app/urls.py
    from django.urls import path
    from .views import Testcheck, Testverify

    urlpatterns += [
        path('testcheck/', Testcheck.as_view()),
        path('testverify/', Testverify.as_view()),
    ]
    ```

### ۲. نحوه استفاده

* **ایجاد پرداخت**: یک درخواست `POST` به آدرس `/testcheck/` ارسال کنید. پاسخی شامل `redirect_url` برای هدایت کاربر به صفحه پرداخت زرین‌پال دریافت خواهید کرد.

* **تایید پرداخت**: پس از پرداخت، زرین‌پال کاربر را به آدرس `/testverify/` بازمی‌گرداند تا تراکنش به صورت خودکار تایید شود. دستورات `redirect()` در ویوی `Testverify` را تغییر دهید تا کاربر به صفحات فرانت‌اند شما (مانند صفحه موفقیت یا شکست) هدایت شود.

### ۳. حالت سندباکس (برای تست)

* فایل `zarinpal.py` را باز کرده و متغیر `SANDBOX` را برابر با `True` قرار دهید.
* در حالت سندباکس می‌توانید از یک UUID تصادفی به عنوان `ZARINPAL_MERCHANT_ID` استفاده کنید.

---
## <a name="english"></a><img src="https://github.com/joielechong/iso-country-flags-svg-collection/blob/master/svg/country-4x3/us.svg" width="24" alt="USA Flag"> Quickstart (English)

### 1. Setup

* **Place Files**: Put `zarinpal.py` in your project. The `views.py` and `urls.py` contain example code to be adapted into your app.

* **Install Dependencies**: For a new project, install all dependencies.
    ```bash
    pip install requests
    pip install djangorestframework
    ```

* **Configure `settings.py`**: Add your Zarinpal Merchant ID and base URL. Using environment variables is highly recommended.
    ```python
    # settings.py
    ZARINPAL_MERCHANT_ID = 'YOUR_ZARINPAL_MERCHANT_ID'
    BASE_URL = 'http://127.0.0.1:8000' # Use your domain in production
    ```

* **Configure `urls.py`**:
    ```python
    # your_app/urls.py
    from django.urls import path
    from .views import Testcheck, Testverify

    urlpatterns += [
        path('testcheck/', Testcheck.as_view()),
        path('testverify/', Testverify.as_view()),
    ]
    ```

### 2. Usage

* **Create Payment**: Send a `POST` request to `/testcheck/`. It returns a `redirect_url` to Zarinpal's payment page.

* **Verify Payment**: After payment, Zarinpal redirects the user to `/testverify/` where the transaction is automatically verified. Modify the `redirect()` calls in `Testverify` to point to your frontend pages (e.g., success or failure pages).

### 3. Sandbox Mode (for Testing)

* Open `zarinpal.py` and set `SANDBOX = True`.
* You can use any random UUID as your `ZARINPAL_MERCHANT_ID` in sandbox mode.
