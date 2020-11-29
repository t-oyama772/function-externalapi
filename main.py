import requests
from google.cloud import storage

def external_api_req(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket('from_gcf')
    print('Bucket {} get.'.format(bucket.name))

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        URL = 'https://api.icndb.com/jokes/random/'
        r = requests.get(URL)
        return r.text
