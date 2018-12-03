import paypalrestsdk
from paypalrestsdk import Payment

paypalrestsdk.configure({
  'mode': 'sandbox', #sandbox or live
  'client_id': 'AQrPPhccbqPZnRWXotX-ZRKaYzeqMVnyMEebQhzDZ0bJ6iVhZviZihTf1ttR5g2eV6JkeDxslJDP2WfK',
  'client_secret': 'YEEP4dANRi_iyuZeDhKgrRtCV7da-wv-wh_fE3OXUElddKl0CNND-Ce9P3viE4CXfprK9CDzlg_TgVgCW' })

def define_payment(amount, userid, date):

    # Create payment object
    payment = Payment({
      "intent": "sale",

      # Set payment method
      "payer": {
        "payment_method": "paypal"
      },

      # Set redirect URLs
      "redirect_urls": {
        "return_url": "http://localhost:3000/process",
        "cancel_url": "http://localhost:3000/cancel"
      },

      # Set transaction object
      "transactions": [{
        "amount": {
          "total": "{}".format(amount),
          "currency": "USD"
        },
        "description": "Payment for User {}, made for {} Period".format(userid, date)
      }]
    })

    return payment

def create_payment(payment):
    # Create payment
    if payment.create():
      # Extract redirect url
      for link in payment.links:
        if link.method == "REDIRECT":
          # Capture redirect url
          redirect_url = (link.href)
          return redirect_url
          # Redirect the customer to redirect_url
    else:
      print("Error while creating payment:")
      print(payment.error)



def execute_payment(payment):
    # Payment ID obtained when creating the payment (following redirect)
    payment = Payment.find("{}".format(payment.id))

    # Execute payment with the payer ID from the create payment call (following redirect)
    if payment.execute({"payer_id": "{}".format(payment.payerid)}):
      print("Payment[%s] execute successfully" % (payment.id))
      return 'success'
    else:
      print(payment.error)
      return 'failure'
