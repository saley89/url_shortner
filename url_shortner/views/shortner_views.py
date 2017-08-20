import json

from flask import Response, request
from werkzeug.utils import redirect

from url_shortner import app
from url_shortner.service.shorten_service import ShortenService


@app.route("/shorten_url", methods=['POST'])
def shorten_url():
    shorten_service = ShortenService()
    is_valid, msg = shorten_service.validate(request)
    if is_valid:
        url = json.loads(request.data)['url']
        identifier = shorten_service.store_url(url)
        data = {'shortened_url': 'http://localhost:8000/{}'.format(identifier)}
        return Response(content_type='application/json', response=json.dumps(data), status=201)
    return Response(content_type='application/json', response=json.dumps({'error': msg}), status=400)


@app.route("/<identifier>", methods=['GET'])
def redirect_url(identifier):
    shorten_service = ShortenService()
    url = shorten_service.retrieve_url(identifier)
    if url:
        return redirect(url, code=302)
    msg = "short url '{}' not found".format(identifier)
    return Response(content_type='application/json', response=json.dumps({'error': msg}), status=404)


@app.errorhandler(Exception)
def handle_unexpected_errors(e):
    msg = "Unexpected exception occurred: {}".format(str(e))
    return Response(content_type='application/json', response=json.dumps({'error': msg}), status=500)
