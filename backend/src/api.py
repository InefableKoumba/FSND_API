import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks")
def get_drinks():
    try:
        data = Drink.query.all()
        drinks = []
        for drink in data:
            drinks.append(drink.short())

        return jsonify({"success": True, "drinks": drinks}), 200
    except:
        return jsonify({"success": False}), 500


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    try:
        data = Drink.query.all()
        drinks = []
        for drink in data:
            drinks.append(drink.long())

        return jsonify({"success": True, "drinks": drinks}), 200
    except:
        return jsonify(({"success": False})), 500


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks", methods=["POST"])
@requires_auth('post:drinks')
def create_drink(jwt):
    if not request.get_json():
        return jsonify({"success": False}), 400
    try:
        data = request.get_json()
        title = data["title"]
        recipe = json.dumps(data["recipe"])
        drink = Drink(title=title, recipe=recipe)
        drink.insert()

        return jsonify({"success": True, "drinks": [drink.long()]}), 200
    except:
        return jsonify({"success": False}), 500


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    if not request.get_json():
        return jsonify({"success": False}), 400
    try:
        data = request.get_json()
        title = data["title"]
        recipe = json.dumps(data["recipe"])

        drink = Drink.query.get(id)
        drink.title = title
        drink.recipe = recipe

        drink.update()

        return jsonify({"success": True, "drinks": [drink.long()]}), 200
    except:
        return jsonify({"success": False}), 500


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    try:
        drink = Drink.query.get(id)
        drink.delete()
        return jsonify({"success": True, "delete": id}), 200
    except:
        return jsonify({"success": False}), 500


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def ressourcenotfound(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Ressources not found"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(401)
def ressourcenotfound(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Not authenticated"
    }), 401
