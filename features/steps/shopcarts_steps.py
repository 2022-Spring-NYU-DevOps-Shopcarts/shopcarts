"""
Shopcart Steps

Steps file for Shopcart.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect

@given('a set of items in shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the shopcarts and delete them one by one
    context.resp = requests.get(context.base_url + '/shopcarts')
    expect(context.resp.status_code).to_equal(200)
    for shopcart in context.resp.json():
        context.resp = requests.delete(context.base_url + '/shopcarts/' + str(shopcart["user_id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new shopcarts
    create_url = context.base_url + '/shopcarts'
    for row in context.table:
        data = {
            "item_id": int(row['item_id']),
            "item_name": row['item_name'],
            "quantity": int(row['quantity']),
            "price": float(row['price']),
            "hold": bool(row['hold'] in ['True', 'true', '1'])
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url+"/"+row['user_id']+"/items", data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
