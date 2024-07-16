from flask import Flask, request, jsonify
from flask_cors import CORS
from Restaurent.logging.logging_module import log
from constants import ORDERS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    """
    Home route that returns a welcome message.
    """
    log.info("Home endpoint accessed")
    return "Welcome to KXN Technologies!"


@app.route('/order/<int:order_id>', methods=['GET'])
def get_single_order(order_id):
    """
    Get single order details by order_id.

    Args:
        order_id (int): The ID of the order.

    Returns:
        JSON response with order details or error message.
    """
    try:
        log.info(f"Fetching order {order_id} started")
        order = ORDERS.get(order_id)
        if order:
            log.info(f"Order found: {order}")
            return jsonify(order)
        else:
            log.warning(f"Order not found: {order_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error fetching order {order_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Fetching order {order_id} ended")


@app.route('/orders', methods=['GET'])
def get_all_orders():
    """
    Get all order details.

    Returns:
        JSON response with all orders.
    """
    try:
        log.info("Fetching all orders started")
        return jsonify(ORDERS)
    except Exception as e:
        log.error(f"Error fetching all orders: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info("Fetching all orders ended")


@app.route('/order', methods=['POST'])
def create_order():
    """
    Create a new order.

    Request Body:
        JSON object with the category of the order.

    Returns:
        JSON response with the new order ID and status message.
    """
    try:
        log.info("Creating order started")
        new_order = request.json
        order_id = len(ORDERS) + 1
        ORDERS[order_id] = {"category": new_order["category"], "status": "Preparing"}
        log.info(f"Order created: {ORDERS[order_id]}")
        return jsonify({"order_id": order_id, "status": "Order received"}), 201
    except Exception as e:
        log.error(f"Error creating order: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info("Creating order ended")


@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Update the status of an order by order_id.

    Args:
        order_id (int): The ID of the order to update.

    Request Body:
        JSON object with the new status.

    Returns:
        JSON response with the updated order status or error message.
    """
    try:
        log.info(f"Updating order {order_id} started")
        if order_id in ORDERS:
            ORDERS[order_id]["status"] = request.json["status"]
            log.info(f"Order updated: {ORDERS[order_id]}")
            return jsonify({"order_id": order_id, "status": "Order updated"})
        else:
            log.warning(f"Order not found: {order_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error updating order {order_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Updating order {order_id} ended")


@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an order by order_id.

    Args:
        order_id (int): The ID of the order to delete.

    Returns:
        JSON response with the status of the deletion or error message.
    """
    try:
        log.info(f"Deleting order {order_id} started")
        if order_id in ORDERS:
            del ORDERS[order_id]
            log.info(f"Order deleted: {order_id} and remaining orders are {ORDERS}")
            return jsonify({"status": "Order deleted"})
        else:
            log.warning(f"Order not found: {order_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error deleting order {order_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Deleting order {order_id} ended")


if __name__ == '__main__':
    app.run(debug=True)
