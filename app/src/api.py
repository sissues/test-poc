from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

users = []
items = []
borrowing_history = []


@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = str(uuid.uuid4())
    user = {
        "user_id": user_id,
        "name": data['name'],
        "email": data['email'],
        "membership_type": data['membership_type']
    }
    users.append(user)
    return jsonify(user), 201


@app.route('/items/<int:item_id>/borrow', methods=['POST'])
def borrow_item(item_id):
    data = request.get_json()
    user_id = data['user_id']
    item_type = data['item_type']
    user = next((u for u in users if u['user_id'] == user_id), None)

    if user:
        borrowing_history.append({
            "user_id": user_id,
            "item_id": item_id,
            "item_type": item_type,
            "borrowed_date": "2023-01-01"
        })
        return jsonify({"status": "borrowed", "user_id": user_id}), 200
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/items/<int:item_id>/return', methods=['POST'])
def return_item(item_id):
    data = request.get_json()
    user_id = data['user_id']

    history_entry = next((h for h in borrowing_history if h['user_id'] == user_id and h['item_id'] == item_id), None)

    if history_entry:
        history_entry['returned_date'] = "2023-02-01"
        return jsonify({"status": "available"}), 200
    else:
        return jsonify({"error": "Item not found"}), 404


@app.route('/users/<user_id>/history', methods=['GET'])
def user_history(user_id):
    user_history = [h for h in borrowing_history if h['user_id'] == user_id]
    return jsonify(user_history), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
