from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/register": {"origins": "http://localhost:63342"},
                     r"/users/*": {"origins": "http://localhost:63342"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)

    dob = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mobile_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    id_type = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(50), nullable=False)
    issued_authority = db.Column(db.String(100), nullable=False)
    issued_state = db.Column(db.String(100), nullable=False)
    issued_date = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(50), nullable=False)
    address_type = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    block_number = db.Column(db.String(20), nullable=False)
    ward_number = db.Column(db.String(20), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    grandfather_name = db.Column(db.String(100), nullable=False)
    spouse_name = db.Column(db.String(100), nullable=True)
    father_in_law_name = db.Column(db.String(100), nullable=True)
    mother_in_law_name = db.Column(db.String(100), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Ensure required fields are present
    required_fields = ['full_name', 'dob', 'email', 'mobile_number', 'gender', 'occupation', 'id_type', 'id_number',
                       'issued_authority', 'issued_state', 'issued_date', 'expiry_date', 'address_type', 'nationality',
                       'state', 'district', 'block_number', 'ward_number', 'father_name', 'mother_name', 'grandfather_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Create a new user instance
    user = User(
        full_name=data['full_name'],
        dob=data['dob'],
        email=data['email'],
        mobile_number=data['mobile_number'],
        gender=data['gender'],
        occupation=data['occupation'],
        id_type=data['id_type'],
        id_number=data['id_number'],
        issued_authority=data['issued_authority'],
        issued_state=data['issued_state'],
        issued_date=data['issued_date'],
        expiry_date=data['expiry_date'],
        address_type=data['address_type'],
        nationality=data['nationality'],
        state=data['state'],
        district=data['district'],

        block_number=data['block_number'],
        ward_number=data['ward_number'],
        father_name=data['father_name'],
        mother_name=data['mother_name'],
        grandfather_name=data['grandfather_name'],
        spouse_name=data.get('spouse_name'),
        father_in_law_name=data.get('father_in_law_name'),
        mother_in_law_name=data.get('mother_in_law_name')
    )

    # Add and commit to the database
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/users', methods=['GET'])
def view_users():
    users = User.query.all()
    user_list = [{
        "id": user.id,
        "full_name": user.full_name,
        "dob": user.dob,
        "email": user.email,
        "mobile_number": user.mobile_number,
        "gender": user.gender,
        "occupation": user.occupation,
        "id_type": user.id_type,
        "id_number": user.id_number,
        "issued_authority": user.issued_authority,
        "issued_state": user.issued_state,
        "issued_date": user.issued_date,
        "expiry_date": user.expiry_date,
        "address_type": user.address_type,
        "nationality": user.nationality,
        "state": user.state,
        "district": user.district,
        "block_number": user.block_number,
        "ward_number": user.ward_number,
        "father_name": user.father_name,
        "mother_name": user.mother_name,
        "grandfather_name": user.grandfather_name,
        "spouse_name": user.spouse_name,
        "father_in_law_name": user.father_in_law_name,
        "mother_in_law_name": user.mother_in_law_name
    } for user in users]

    return jsonify(user_list), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404  # Return error if user doesn't exist

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200


if __name__ == "__main__":
    app.debug = True  # Enable debug mode
    app.run()
