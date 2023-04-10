from locale import currency
import stripe
import os
import time
from dotenv import load_dotenv


load_dotenv()

def create_payemnt(price):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    s = stripe.checkout.Session.create(

        success_url = 'https://google.com',
        cancel_url = 'https://google.com',
        mode= 'payment',
        customer_email = None,
        expires_at = int(time.time()) + 1800,
        line_items = [{'price_data':{'currency':'EUR', 'product_data':{'name':'Sayous Booking'}, 'unit_amount':price}, 'quantity':1}])

    print(s['url'])
    return s['url']
