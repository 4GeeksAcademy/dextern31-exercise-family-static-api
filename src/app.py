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
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    


    return jsonify(members), 200

@app.route("/member/<int:member_id>", methods=["GET"])
def getSingleMember(member_id):
    member = jackson_family.get_member(member_id)
    if(member is None):
        return jsonify({"msg": "member don't exist"}), 400
    new_member = {
        "id": member["id"],
        "first_name": member["first_name"],
        "age": member["age"],
        "lucky_numbers": member["lucky_numbers"]
    }
    

    return jsonify(new_member), 200

@app.route("/member", methods=["POST"])
def addMember():
    request_body = request.get_json()
    newID = request_body.get("id")
    if newID is None:
        newID = jackson_family._generateId()

    member = {
        "id": newID,
        "first_name": request_body.get("first_name"),
        "age": request_body.get("age"),
        "lucky_numbers": request_body.get("lucky_numbers")
    }
    
    jackson_family.add_member(member)

    return jsonify({"msg": "family member added"}), 200

@app.route("/member/<int:member_id>", methods=["DELETE"])
def deleteMember(member_id):
    jackson_family.delete_member(member_id)
    
    response_body = {
        "done": True
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
