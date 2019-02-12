import logging
from flask import (
    Flask,
    request,
    Response
)

import requests

app = Flask(__name__)

@app.route('/<path:url>', methods=['GET', 'POST', 'PUT', 'PATCH'])
def proxy(url):
    # extract the request info and change its destination

    # how to deal with socketio
    if url == "socket.io/":
        target = request.base_url
    else:
        # target = f"http://localhost:80/{url}"
        target = f"http://www.google.com/{url}"

    data = request.data or request.form
    logging.debug(f'url: {url}, target: {target}')
    truely_request = requests.Request(method=request.method, url=target, headers=request.headers, data=data, cookies=request.cookies)
    resp = requests.Session().send(truely_request.prepare())
    logging.debug(resp.content)
    response = app.make_response((resp.content, resp.status_code, resp.headers.items()))
    
    for k, v in resp.cookies:
        response.set_cookie(k, v)

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
