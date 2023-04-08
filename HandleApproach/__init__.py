import azure.functions as func
from azf_wsgi import AzureFunctionsWsgi
from FlaskApp import app

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

# def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
#     return AzureFunctionsWsgi(app, False).main(req, context)