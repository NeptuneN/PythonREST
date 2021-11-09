import os
FAUNA_SECRET = os.environ.get('fnAEXl9qnYAAw6OfhM7tKK52kCJpiIatmG2muo9h')

import flask
from flask import request

import faunadb
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/signup', methods=['POST'])
def signup():

    body = request.json
    client = FaunaClient(
      secret=FAUNA_SECRET,
      domain="db.eu.fauna.com",
      port=8080,
      scheme="https"
    )

    try:
        result = client.query(
            q.create(
                q.collection("Users"),
                {
                    "data": {
                        "username": body["username"]
                    },
                    "credentials": {
                        "password": body["password"]
                    }
                }
            )
        )

        return {
            "userId": result['ref'].id()
        }

    except faunadb.errors.BadRequest as exception:
        error = exception.errors[0]
        return {
            "code": error.code,
            "description": error.description
        }, 409

@app.route('/login', methods=['POST'])
def login():

    body = request.json
    client = FaunaClient(secret=FAUNA_SECRET)

    try:
        result = client.query(
            q.login(
                q.match(
                    q.index("Users_by_username"),
                    body["username"]
                ),
                {"password": body["password"]}
            )
        )

        return {
            "secret": result['secret']
        }

    except faunadb.errors.BadRequest as exception:
        error = exception.errors[0]
        return {
            "code": error.code,
            "description": error.description
        }, 401

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))