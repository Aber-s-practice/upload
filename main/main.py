import os
import time
from os import path
from subprocess import Popen
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from .config import Media_DIR, BASE_DIR, Media_URL

app = Sanic()


def push(filename: str) -> None:
    Popen(f'git add {filename} && git commit -m "Auto commit" && git push && rm -f {filename}', cwd=Media_DIR, shell=True)


@app.listener('before_server_start')
def try_pull(app, loop):
    if not path.exists(Media_DIR):
        Popen('git pull https://git.dev.tencent.com/AberSheeran/image.git', cwd=path.dirname(Media_DIR), shell=True)


class IndexView(HTTPMethodView):

    async def get(self, request):
        return await response.file(path.join(path.join(BASE_DIR, "template"), "index.html"))

    async def post(self, request):
        image = request.files.get('image')
        timestamp = "".join(str(time.time()).split(".")) + "." + image.name.split(".")[-1]
        target = path.join(Media_DIR, timestamp)
        if path.exists(target):
            return response.json({"received": True, "code": 701, "message": "File already exists!"})
        with open(target, "wb") as file:
            file.write(image.body)
        push(timestamp)
        return response.json({"received": True, "code": 200, "url": Media_URL + timestamp})


app.add_route(IndexView.as_view(), "/image")
app.static('/static', path.join(path.join(BASE_DIR, "template"), "static"))
app.static('/favicon.ico', path.join(BASE_DIR, 'favicon.ico'), name='favicon.ico')
