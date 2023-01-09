import json, requests
from urllib.parse import urlencode
from flask import render_template, abort, redirect, request
from pay_flask import app

products = {
    'ipad': {
        'name': 'ipad',
        'price': 300000,
    },
    'Music': {
        'name': 'Music',
        'price': 20000,
    },
    'Movie': {
        'name': 'Movie',
        'price': 200000,
    },    
    'Car': {
        'name': 'Car',
        'price': 20000000,
    },
}

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/order/<product_id>', methods=['POST'])
def order(product_id):
    if product_id not in products:
        abort(404)
    auth_headers ={
        "Authorization": "Bearer sk_test_7e747d8832ca52dad6639c6f2b7042e10c5fb6eb",
        "Content-Type": "application/json"
    }
    auth_data = { "email": "customer@email.com", "amount": "{}".format(products[product_id]['price']) }
    auth_data = json.dumps(auth_data)
    req = requests.post('https://api.paystack.co/transaction/initialize', headers=auth_headers, data=auth_data)
    response_data = json.loads(req.text)
    paystack_uri = response_data['data']['authorization_url']
    return redirect(paystack_uri)

@app.route('/callback')
def order_success():
    ref = request.args['trxref']
    auth_headers ={
        "Authorization": "Bearer sk_test_7e747d8832ca52dad6639c6f2b7042e10c5fb6eb",
        "Content-Type": "application/json"
    }
    req = requests.get('https://api.paystack.co/transaction/verify/{}'.format(ref), headers=auth_headers)
    tr_data = json.loads(req.text)
    message = tr_data['data']['status']
    amount = tr_data['data']['amount']
    amount = (amount/100)
    amount = "{:.2f}".format(amount)
    tr_id = tr_data['data']['id']
    return render_template('success.html', tr_id=tr_id, message=message, amount=amount)
