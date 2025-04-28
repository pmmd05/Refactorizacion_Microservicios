from faker import Faker
from flask import Flask, jsonify
import logging


app = Flask(__name__)
data = []
fake = Faker()


@app.route('/items', methods=['GET'])
def list_items():
    """Devuelve todos los ítems"""
    return jsonify(data), 200


@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    """Devuelve un ítem por ID"""
    return jsonify(data[id]), 200


def create_items(num):
    return {
        'id': num,
        'desc': fake.bs()
    }


def create_data():
    return [create_items(num) for num in range(1, 100)]


if __name__ == '__main__':
    data = create_data()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='0.0.0.0')
