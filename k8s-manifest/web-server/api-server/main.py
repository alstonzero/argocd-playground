import os
from flask import Flask, make_response, request, redirect

app = Flask(__name__)
LOCAL_DIRECTORY = '/htdocs'


@app.route('/latest')
def return_latest_file():
    def _redirect(localpath):
        path = localpath.replace(LOCAL_DIRECTORY, '')
        host = request.headers.get('X-Forwarded-Host', '11.0.1.228')
        return redirect(f'http://{host}{path}')

    res = make_response()

    path = request.args.get('path', '').split('/')
    filename = request.args.get('filename', '').split('/')

    if len(path) == 0:
        res.status = '404'
        return res

    path = os.path.join(LOCAL_DIRECTORY, *path)

    try:
        directories = sorted([os.path.join(path, d) for d in os.listdir(path)],
                             key=os.path.getmtime,
                             reverse=True)

        if len(filename) == 0:
            return _redirect(directories[0])

        for directory in directories:
            fullpath = os.path.join(directory, *filename)
            if os.path.exists(fullpath):
                return _redirect(fullpath)

        res.status = '404'
    except FileNotFoundError:
        res.status = '404'

    return res


@app.route('/')
def hello():
    return 'Hello world.'


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
