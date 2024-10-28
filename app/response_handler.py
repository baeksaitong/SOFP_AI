from flask import jsonify

def create_response(data=None, error=None, status=200):
    """JSON 응답을 생성하여 반환"""
    if error:
        response = {'error': error}
    else:
        response = data
    return jsonify(response), status
