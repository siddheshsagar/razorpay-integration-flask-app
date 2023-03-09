Razorpay Test App for Python

-> Sample App for Razorpay Python Integration

# DEPLOYMENT ERRORS

When deploying the flask app to azure web app, one might face problem where the web app will give the 
"Application Error" or the web app will not run properly.
Here if your flask app is running properly in your local environment, it might be the case that web app is not able to call the flask app. you can then setup startup command.

web app -> configurations -> general settings -> Startup Command

In the Startup Command box you can add the file name where the startup command for your flask is written or you can simply write that command in that box as well.
I have used gunicorn server so I write command as below:

gunicorn --bind=0.0.0.0 --timeout 600 app:app

where ist 'app' is app.py which is the file where the flask code is written and 2nd 'app' is the flask app instance name.


# NOTES: 

1. I have used pthon's 'pyodbc' module to connect with the azure sql database in my flask app code. while in the local development phase, i needd to download a driver ("ODBC Driver 18 for SQL Server") for the working of the pyodbc module. But I didn't needed to download it seperatly for the web app. seems like web app automatically(somehow) manage to connect with the database.
