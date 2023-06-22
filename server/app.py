from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [message.serialize() for message in messages]
    return jsonify(messages_list)




@app.route('/messages', methods=['POST'])
def create_message():
    body = request.form.get('body')
    username = request.form.get('username')

    if not body or not username:
        return make_response(jsonify({'error': 'Missing parameters'}), 400)

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()

    return jsonify(message.serialize())


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    body = request.form.get('body')

    if not body:
        return make_response(jsonify({'error': 'Missing parameter'}), 400)

    message.body = body
    db.session.commit()

    return jsonify(message.serialize())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted'})

if __name__ == '__main__':
    app.run(port=5555)
