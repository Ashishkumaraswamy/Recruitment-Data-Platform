from flask import jsonify


class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    INTERNAL_SERVER_ERROR = 500
    FORBIDDEN = 403


def response(msg, code):
    return jsonify({
        'message': msg
    }), code
