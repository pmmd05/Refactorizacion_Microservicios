from flask import Flask, json, jsonify, request
import logging
import requests

# Inicializa la aplicación Flask
app = Flask(__name__)

# =========================
# Endpoint: GET /orders
# =========================
@app.route('/orders', methods=['GET'])
def orders():
    """
    Devuelve la lista de órdenes.
    Parámetros de consulta:
      - count (opcional): número máximo de órdenes a devolver.
    """
    # Lee el parámetro 'count' de la query string (por ejemplo ?count=10)
    count = request.args.get('count')

    # Llama al Orders Service para obtener todas las órdenes
    data = requests.get('http://demo_orders:5000/orders').json()

    # Si se especificó 'count', recorta la lista a esa cantidad
    if count:
        return jsonify(data[:int(count)]), 200
    # Si no, devuelve todas las órdenes
    else:
        return jsonify(data), 200

# ==========================================
# Endpoint: GET /detail/<order_id>
# ==========================================
@app.route('/detail/<int:order_id>', methods=['GET'])
def detail(order_id):
    """
    Devuelve el detalle completo de una orden,
    incluyendo los datos de los ítems asociados.
    """
    # Llama al Aggregate Service para obtener la orden con sus ítems detallados
    data = requests.get(
        f'http://demo_aggregate:5000/orders/{order_id}/detail'
    ).json()

    # Retorna el JSON tal cual lo devuelve el Aggregate Service
    return jsonify(data), 200

# ==========================================
# Endpoint: GET /items
# ==========================================
@app.route('/items', methods=['GET'])
def items():
    """
    Proxy al Items Service:
    Devuelve la lista de todos los ítems.
    """
    # Llama al Items Service para obtener la lista de ítems
    data = requests.get('http://demo_items:5000/items').json()
    return jsonify(data), 200

# ==========================================
# Endpoint: GET /items/<id>
# ==========================================
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    """
    Proxy al Items Service:
    Devuelve el detalle de un ítem específico por su ID.
    """
    # Llama al Items Service para obtener un único ítem
    data = requests.get(f'http://demo_items:5000/items/{id}').json()
    return jsonify(data), 200

# =========================
# Arranque de la aplicación
# =========================
if __name__ == '__main__':
    # Configura el nivel de logging a INFO para ver peticiones y respuestas
    app.logger.setLevel(logging.INFO)
    # Ejecuta la app en modo debug y la expone en todas las interfaces de red
    app.run(debug=True, host='0.0.0.0')

