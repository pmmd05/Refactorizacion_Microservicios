from flask import Flask, jsonify, request
import logging
import requests

# Se crea la aplicación Flask
app = Flask(__name__)

# Ruta para obtener el detalle de una orden específica, incluyendo información de ítems
@app.route('/orders/<int:order_id>/detail', methods=['GET'])
def order_detail(order_id):
    """Obtiene la orden con los detalles completos de los ítems"""
    # Se realiza una solicitud al servicio de órdenes para obtener la información de una orden específica
    order = requests.get(
        f'http://demo_orders:5000/orders/{order_id}'
    ).json()

    # Para cada ítem en la orden, se consulta su detalle en el servicio de ítems
    items = [_fetch_item(item_id) for item_id in order.get('items', [])]

    # Se reemplaza la lista de IDs de ítems con los objetos de ítems detallados
    del order['items']
    order['items'] = items

    # Se devuelve la orden enriquecida con el detalle de los ítems
    return jsonify(order), 200

# Función auxiliar para obtener el detalle de un ítem
def _fetch_item(item_id):
    """Obtiene la información de un ítem específico desde el servicio de ítems"""
    return requests.get(
        f'http://demo_items:5000/items/{item_id}'
    ).json()

# Inicialización de la aplicación
if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)  # Configura el nivel de logs a INFO
    app.run(debug=True, host='0.0.0.0')  # Ejecuta la aplicación escuchando en todas las interfaces
