#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict(rules=('-baked_goods',)) for bakery in bakeries]
    
    response = make_response(
        jsonify(bakeries_list),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = db.session.get(Bakery, id)
    if not bakery:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)
    bakery_data = bakery.to_dict(rules=('-baked_goods.bakery',))
    
    response = make_response(
        jsonify(bakery_data),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict(rules=('-bakery.baked_goods',)) for baked_good in baked_goods]
    
    response = make_response(
        jsonify(baked_goods_list),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_data = baked_good.to_dict(rules=('-bakery.baked_goods',)) if baked_good else {}

    response = make_response(
        jsonify(baked_good_data),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
