from __future__ import print_function

import os
import json
import requests

from flask import Flask, request

app = Flask(__name__)

generic_url = 'https://%(cluster)s/oapi/v1/namespaces/%(project)s/buildconfigs/%(application)s/webhooks/%(authorization)s/generic'

@app.route('/travis-ci/<cluster>/<project>/<application>', methods=['POST'])
def webhook_travis_ci(cluster, project, application):
    debug = os.environ.get('DEBUG', '').lower() in ('1', 'true')

    authorization = request.headers['Authorization']

    fields = json.loads(request.form['payload'])

    if debug:
        print('inbound-authorization:', authorization)
        print('inbound-payload:', fields)

    if fields['status'] not in ('0', None):
        return ''

    url = generic_url % dict(cluster=cluster, project=project,
            application=application, authorization=authorization)

    payload = {}

    payload['type'] = 'git'

    payload['git'] = dict(
        uri=fields['repository']['url'],
        refs='refs/heads/'+fields['branch'],
        commit=fields['commit'],
        author=dict(
            name=fields['author_name'],
            email=fields['author_email']
        ),
        committer=dict(
            name=fields['committer_name'],
            email=fields['committer_email']
        ),
        message=fields['message']
    )

    headers = {}
    headers['Content-Type'] = 'application/json'

    data = json.dumps(payload)

    verify = not(os.environ.get('SSL_NO_VERIFY', '').lower() in ('1', 'true'))

    if debug:
        print('outbound-url:', url)
        print('outbound-payload:', payload)
        print('outbound-verify:', verify)

    try:
        response = requests.post(url, verify=verify, headers=headers, data=data)

    except Exception as e:
        print(e)

        raise

    return ''

@app.route('/')
def hello():
    return 'OpenShift Rocks!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
