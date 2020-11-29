import requests
from datetime import datetime, timedelta, timezone
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

    JST = timezone(timedelta(hours=+9), 'JST')
    dt_now = datetime.now(JST)
    dt_now_str = dt_now.strftime('%Y%m%d-%H%M%S')

    bucket_name = 'from_gcf'
    file_name = 'test_' + dt_now + '.txt'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    # bucket = storage_client.get_bucket(bucket_name)
    print('Bucket {} get.'.format(bucket.name))
    blob = bucket.blob(file_name)

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        URL = 'https://api.icndb.com/jokes/random/'
        r = requests.get(URL)
        blob.upload_from_string(r.text)
        return r.text
