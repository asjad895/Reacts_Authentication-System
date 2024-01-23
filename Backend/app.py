from flask import Flask
import json,requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.models import User,Base 
from app.views.email import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from app.utils.helpers import *
from flask_migrate import Migrate, migrate

# main api development
app = Flask(__name__)
CORS(app) 
# databse setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db=SQLAlchemy(app)
# database tables if they don't exist
Base.metadata.create_all(engine)  
# Use the session factory to create sessions for interacting with the database
session = Session()
migrate = Migrate(app, db)

# api
@app.route('/')
def home():
	return 'Flask is working'

@app.route('/register',methods=['POST'])
def Register():
    try:
        # Get JSON data from request
        data = request.get_json()
        user=data['username']
        email=data['email']
        print("Received JSON data:", data)
        # Create a new user instance
        new_user = User(user_name=user,email=email,hash_password=data['password'] )
        session.add(new_user)
        session.commit()
        # send_verification_email(user=user,email=email)
        print("email sent......")
        return jsonify({'sucess': 'User created successfully'}), 201
    except IntegrityError as e:
        # duplicate
        print(e)
        session.rollback()
        return jsonify({'error': 'username already exists'}), 400

    except Exception as e:
        # other unexpected errors
        print(e)
        session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print("recived data",data)
        if 'username' not in data or 'password' not in data:
            raise ValueError('Username and password are required.')
        username = data['username']
        password = data['password']
        try:
            # Query the database 
            tuser = session.query(User).filter(User.user_name == username).first()
            print("fetch data",tuser)
            user_dict = serialize_model(tuser)
            print(user_dict)
        except Exception as e:
            print(e)
            return jsonify({'message': 'An unexpected error occurred in fetching.', 'success': False}), 500
        
        if tuser and user_dict['hash_password'] == password:
            return jsonify({'message': 'Login successful.', 'success': True}), 200
        else:
            return jsonify({'message': 'Invalid username or password.', 'success': False}), 401

    except ValueError as e:
        return jsonify({'message': str(e), 'success': False}), 400

    # except Exception as e:
    #     print(e)
    #     return jsonify({'message': 'An unexpected error occurred.', 'success': False}), 500

        
@app.route('/users', methods=['GET'])
def FetchAllUsers():
    try:
        tuser = session.query(User).all()
        print("fetch data",tuser)
            # Convert the query results to a list of dictionaries
        result = [{'id': user.id, 'username': user.user_name, 'email':user.email,'password': user.hash_password} for user in tuser]
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An unexpected error occurred in fetching.', 'success': False}), 500
    
@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    user=session.query(User).filter(User.user_name==username).first()
    if user:
        user_data = {'name': user.user_name, 'email': user.email, 'password': user.hash_password}
        return jsonify(user=user_data)
    else:
        return jsonify({'message': 'User not found'}), 404
    
@app.route('/email/<username>', methods=['POST'])
def email_to_user(username):
    user = session.query(User).filter(User.user_name == username).first()
    print(user)
    if user:
        reset_url="http://localhost:3000/reset"
        url = "https://api2.juvlon.com/v4/httpSendMail"
        email=user.email
        print(email)
        data = {
            "ApiKey": "OTg5NjQjIyMyMDI0LTAxLTIxIDE5OjMzOjQ5",
            "requests": [{
                "subject": "Password Reset",  
                "from": "120ad0027@iiitk.ac.in",
                "body": f"Please click this link to reset your password: {reset_url}", 
                "to": user.email
            }]
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise exception for non-200 status codes
            return jsonify({"message": "Password reset email sent. Please check your inbox.", "success": True}), 200

        except requests.exceptions.RequestException as e:
            return jsonify({"message": "Failed to send email. Please try again.", "error": str(e)}), 500
    else:
        return jsonify({"message": "User not found.", "success": False}), 404


@app.route('/reset', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        username = data['username']
        new_password = data['newPassword']
        print("recieved data",new_password)
        if not username or not new_password:
            return jsonify({'message': 'Username and new password are required.', 'success': False}), 400
        user = session.query(User).filter(User.user_name == username).first()
        if not user:
            return jsonify({'message': 'User not found.', 'success': False}), 404
        # Update password in the database
        print(user)
        user.hash_password = new_password
        print(user.hash_password)
        session.commit()
        return jsonify({'message': 'Password reset successful.', 'success': True}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'An unexpected error occurred.', 'success': False}), 500


if __name__ == '__main__':
    app.run(debug=True)