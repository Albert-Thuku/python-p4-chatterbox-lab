from flask import Flask, request, make_response, jsonify, json
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

@app.route('/')
def index():
    return {"message" : "Welcome to chatterbox messages API"}

@app.route('/messages', methods=["GET", "POST"])
def messages():
    messages = Message.query.all()

    if request.method == 'GET':
        message_list = []
        for message in messages:
            message_dict = message.to_dict()
            message_list.append(message_dict)
        
        response = make_response(jsonify(message_list), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    
    if request.method == 'POST':
        body = request.json['body']
        username = request.json['username']

        new_message = Message(
            body=body,
            username=username
        )
        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()
        response = make_response(jsonify(message_dict),200)
        response.headers["Content-Type"] = "application/json"
        return response
    
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = Message.query.filter_by(id=id).first()
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        
        for attr, value in json_data.items():
            setattr(message, attr, value)
        
        db.session.add(message)
        db.session.commit()

        updated_dict = message.to_dict()
        response = make_response(jsonify(updated_dict), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    
    if request.method == 'DELETE':
        message = Message.query.filter_by(id=id).first()
        db.session.delete(message)
        db.session.commit()

        response = make_response('Succesfully deleted',200)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
