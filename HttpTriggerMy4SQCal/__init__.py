import logging

import azure.functions as func
from . import FeedGenerator as feeds

def main(req: func.HttpRequest, calendarBlob: func.Out[bytes]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    year = None
    if (req.params.get('year') is not None):
        year = int(req.params.get('year'))
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
            if (req.params.get('year') is not None):
                year = int(req_body.get('year'))

    if name:
        generator = feeds.FeedGenerator()
        calendar = generator.generate(calendarBlob, year)

        s = ''.join(str(e) for e in calendar)
        return func.HttpResponse(s,mimetype="text/calendar")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
