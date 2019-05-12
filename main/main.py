import os
import time
from functools import wraps
from os import path
from subprocess import Popen
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from .config import MEDIA_DIR, BASE_DIR, MEDIA_URL

app = Sanic()


def DontRunInDebug(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        if app.debug:
            return None
        return func(*args, **kwargs)
    return warpper


@DontRunInDebug
def push(filename: str) -> None:
    if os.name == "posix":
        Popen(f'git add {filename} && git commit -m "Auto commit" && git push && rm -f {filename}', cwd=MEDIA_DIR, shell=True)
    else:
        # 此处不用Popen的原因是非Unix/Linux系统不一定有rm命令
        # 而Popen是启动子进程执行命令, 无法保证在Popen执行完之后再执行os.remove
        _path = os.getcwd()
        os.chdir(MEDIA_DIR)
        os.system(f"git add {filename}")
        os.system('git commit -m "Auto commit"')
        Popen('git push', cwd=MEDIA_DIR, shell=True)
        os.remove(path.join(MEDIA_DIR, filename))
        os.chdir(_path)


@DontRunInDebug
def write(image, target: str) -> None:
    with open(target, "wb+") as file:
        file.write(image.body)


class IndexView(HTTPMethodView):

    async def get(self, request):
        return await response.file(path.join(path.join(BASE_DIR, "template"), "index.html"))

    async def post(self, request):
        image = request.files.get('image')
        timestamp = "".join(str(time.time()).split(".")) + "." + image.name.split(".")[-1]
        target = path.join(MEDIA_DIR, timestamp)
        if path.exists(target):
            return response.json({"received": True, "code": 701, "message": "File already exists!"})
        write(image, target)
        push(timestamp)
        return response.json({"received": True, "code": 200, "url": MEDIA_URL + timestamp})


app.add_route(IndexView.as_view(), "/image")
app.static('/static', path.join(path.join(BASE_DIR, "template"), "static"))
app.static('/favicon.ico', path.join(path.join(path.join(BASE_DIR, "template"), "static"), 'favicon.ico'), name='favicon.ico')
