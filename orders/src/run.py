from faker import Faker
from flask import Flask, jsonify, request
import logging
import random


app = Flask(__name__)
data = []
fake = Faker()


@app.route('/orders', methods=['GET'])
def list_orders():
    return jsonify(data), 200


@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    return jsonify(data[id]), 200


def create_order(num):
    return {
        'id': num,
        'cust': fake.name(),
        'items': [random.randint(1, 100) for _ in range(1, random.randint(1, 10))]
    }


def create_data():
    return [create_order(num) for num in range(1, 1000)]


if __name__ == '__main__':
    data = create_data()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='0.0.0.0')
