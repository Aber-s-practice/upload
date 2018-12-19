from sanic import response
from sanic.exceptions import RequestTimeout, NotFound

from .main import app


@app.exception(RequestTimeout)
def ignore_request_time_out(request, exception):
    pass


@app.exception(NotFound)
async def ignore_404s(request, exception):
    return response.text("What do you want to do?")
