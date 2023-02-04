import razorpay
from flask import Flask, render_template, request
from waitress import serve

razorpay_client = razorpay.Client(auth=("rzp_test_UTtd75CFIcXAzt", "VBB0no9O5Yrbz44NznO7plQA"))
app = Flask(__name__)

@app.route('/')
def app_create():
    # from the checkout page the when the customer hit the "proceed to pay button", a post request will be called to this 
    # endpoind along with the data associated with the purchase.
    
    # this the the temporary data we have provided for testing purpose
    data = {
        "amount" : 40000,
        "currency" : "INR",
        "receipt" : "dynamic_receipt",
        "notes":{
            "name": "Siddhesh",
            "Payment_for":"testing"
        }
    }
    order = razorpay_client.order.create(data=data)
    return render_template('main.html',Order=order)


@app.route('/paymentHandler', methods=['POST'])
def payment_handler():
    response = request.get_json()
    ver = razorpay_client.utility.verify_payment_signature(response)
    return str(ver)


if __name__ == '__main__':
    serve(app,host='0.0.0.0', port=8080)
    # debug="False"
    



