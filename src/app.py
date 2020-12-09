"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def getAll():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def getOne(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member == None:
        return jsonify('Not Found'), 404
    else:
        response_body = {
            "family": member
        }
        return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def addMember():
    body = request.get_json()
    
    if body is None:
        raise APIException("You need to specify the request body as a json object", status_code=400)
    if 'age' not in body:
        raise APIException('You need to specify the age', status_code=400)
    if 'first_name' not in body:
        raise APIException('You need to specify the first name of member', status_code=400)
    if 'last_name' not in body:
        raise APIException('You need to specify the last name of member', status_code=400)
    if 'lucky_numbers' not in body:
        raise APIException('You need to specify the lucky numbers of member', status_code=400)
    
    #get posted data and assign it a variable.
    #check that all attributes are there. (ie. first name, last name, age, lucky numbers, etc...)
    #Pass the information to add member if all required info is there.
    #If not show error
    # this is how you can use the Family datastructure by calling its methods
    jackson_family.add_member(body)
    return "Member added", 200

@app.route('/members/<int:member_id>', methods=['DELETE'])
def deleteMember(member_id):

    # this is how you can use the Family datastructure by calling its methods
    if jackson_family.delete_member(member_id):
        return "Member deleted", 200
    else:
        return "Member not found", 404
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
