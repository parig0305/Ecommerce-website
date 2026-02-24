Razorpay sandbox setup

This project reads Razorpay credentials from environment variables. Add the following variables to your environment before running the server:

- RAZORPAY_KEY_ID
- RAZORPAY_KEY_SECRET
- (optional) RAZORPAY_UPI_ID

Windows PowerShell (temporary for current session):

```powershell
$env:RAZORPAY_KEY_ID = "rzp_test_xxx"
$env:RAZORPAY_KEY_SECRET = "your_test_secret"
$env:RAZORPAY_UPI_ID = "your-upi-id@upi"
# Then run the server in the same shell
env\Scripts\python.exe manage.py runserver
```

Windows CMD (temporary):

```cmd
set RAZORPAY_KEY_ID=rzp_test_xxx
set RAZORPAY_KEY_SECRET=your_test_secret
set RAZORPAY_UPI_ID=your-upi-id@upi
env\Scripts\python.exe manage.py runserver
```

Permanent (recommended for development): store these variables in your system environment or use a `.env` loader. Do NOT commit secrets to version control.

.env support
-----------
You can create a local `.env` file at the project root (copy `.env.example`) and place your keys there. The project will load `.env` automatically when present.

Example `.env` (from `.env.example`):

```
RAZORPAY_KEY_ID=rzp_test_xxx
RAZORPAY_KEY_SECRET=your_test_secret
RAZORPAY_UPI_ID=your-upi-id@upi
```

Testing the flow

1. Create an order in the app (via checkout flow or admin). Note the numeric `Order.id`.
2. Visit `/payments/razorpay/qr/<order_id>/` (replace `<order_id>` with the numeric id) to generate a Razorpay payment link and QR code.
3. Alternatively, from the checkout page choose the Razorpay option which uses `razorpay_payment.html`.

If you want me to run an end-to-end test, provide sandbox keys here or set them in the environment and tell me to run the test. I will not store keys in the repository.
