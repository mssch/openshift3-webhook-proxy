from __future__ import print_function

import os
import sys
import json
import requests

from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

generic_url = 'https://%(cluster)s/oapi/v1/namespaces/%(project)s/buildconfigs/%(application)s/webhooks/%(authorization)s/generic'

@app.route('/gogs/<cluster>/<project>/<application>', methods=['POST'])
def webhook_gogs(cluster, project, application):

    url = generic_url % dict(cluster=cluster, project=project,
            application=application, authorization='ebpiawesomesecret')

    headers = {}
    headers['Content-Type'] = 'application/json'

    try:
        response = requests.post(url, verify=False, headers=headers, data=None)
        #response = requests.post(url, verify=verify, headers=headers, data=data)

    except Exception as e:
        print(e, file=sys.stderr)

        raise

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
