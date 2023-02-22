import razorpay
from flask import Flask, render_template, request
from waitress import serve
import pyodbc
import datetime

razorpay_client = razorpay.Client(auth=("rzp_test_MyVOqc8q5Empfv", "xIQ2HqCdosTCUrrp66bnJNiN"))
app = Flask(__name__)


# azure sql connection 
server = 'hotel-db-server.database.windows.net'
database = 'hotel-user'
username = 'priyonuj'
password = '12345@Asdf'
driver= '{ODBC Driver 18 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) 
cursor = conn.cursor()


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
    data = request.get_json()
    response = data.get('response')
    amount = data.get('amount')
    
    # verify payment signatures
    status = razorpay_client.utility.verify_payment_signature(response)
    if str(status) == "True":
        status = "Done"
    else:
        status = "Failed"
    
    submitted_at = datetime.datetime.now()  
    
    query = "INSERT INTO paymentInfo(razorpay_order_id, razorpay_payment_id, amount, status, submitted_at) VALUES (?, ?, ?, ?, ?)"
    values = (response['razorpay_order_id'], response['razorpay_payment_id'], amount, status, submitted_at)
    cursor.execute(query, values)
    conn.commit()
    
    return status


if __name__ == '__main__':
    # use below in production env
    # to check the app, open http://localhost:8080/
    serve(app,host='0.0.0.0', port=8080)
    
    # use below in development environment
#     app.run(debug="True")
    
    # by default, debug="False"
    





















    



