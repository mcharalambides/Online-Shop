import stripe
import os
import time
from dotenv import load_dotenv
from app import session
from celery import Celery
from app import mydb
from datetime import timedelta,datetime
import pytz

load_dotenv()
# IST = pytz.timezone('Asia/Nicosia')

# celeryApp = Celery('tasks', broker=os.getenv('SQLALCHEMY_DATABASE_URI'))
# celeryApp.conf.update(
#     CELERY_RESULT_BACKEND=os.getenv('SQLALCHEMY_DATABASE_URI'),
#     CELERY_TIMEZONE='Asia/Nicosia'
# )

# @celeryApp.task
# def my_task():
#     print("i am here celery")
#     mydb.execute_update("DELETE FROM tempOrders WHERE UserOrdered='" + session['stripe_session'] + "'")
#     return

def create_payemnt(price, email):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    s = stripe.checkout.Session.create(

        success_url = 'http://mariosch19.pythonanywhere.com/success',
        cancel_url = 'http://mariosch19.pythonanywhere.com/cancel',
        mode= 'payment',
        allow_promotion_codes = True,
        customer_email = email,
        invoice_creation= {"enabled": True},
        expires_at = int(time.time()) + 1800,
        payment_intent_data = {'receipt_email': email},
        line_items = [{'price_data':{'currency':'EUR', 'product_data':{'name':'Sayous Booking'}, 'unit_amount':price*100}, 'quantity':1}])
    
    # celeryApp.conf.beat_schedule = {
    #     'execute_task_at_specific_timestamp': {
    #         'task': 'tasks.my_task',
    #         'schedule': datetime.now(IST) + timedelta(seconds=30),
    #         'args': (),
    #     },
    # }
    
    # my_task.apply_async(eta=datetime.now(IST) + timedelta(seconds=30))
    session['stripe_session'] = s['id']
    print(session['stripe_session'])
    return s['url']
