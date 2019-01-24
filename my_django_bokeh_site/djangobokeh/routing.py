import re
from django.conf.urls import url
from django.apps import apps
from channels.http import AsgiHandler
from bokeh.server.views.doc_handler import DocHandler
from bokeh.server.views.ws import WSHandler

from . import consumers

djangobokeh_app_config = apps.get_app_config('djangobokeh')
all_patterns = djangobokeh_app_config.all_patterns


def _createURLmapping(all_patterns, from_tornado_handler_type, to_channels_consumer_type, url_list):

    for pattern in all_patterns:
        url_str = pattern[0]
        handler_obj = pattern[1]
        kwargs = pattern[2]

        if handler_obj is from_tornado_handler_type:
            if url_str.startswith("/"):
                url_str = url_str[1:]
            if url_str.endswith("/?"):
                url_str = url_str[:-2]
            url_reg_str = r"^bokehapps/" + re.escape(url_str) + r"$"
            url_list.insert(0, url(url_reg_str, to_channels_consumer_type, kwargs=kwargs))


websocket_urlpatterns = [
    #url(r'^sliders/ws$', consumers.BokehAppWebsocketConsumer, kwargs=kwargs),
]

http_urlpatterns = [
    #url(r'^sliders$', consumers.BokehAppHTTPConsumer, kwargs=kwargs),
    url(r"", AsgiHandler),  # other sync urls go to sync handler
]


_createURLmapping(all_patterns, DocHandler, consumers.BokehAppHTTPConsumer, http_urlpatterns)
_createURLmapping(all_patterns, WSHandler, consumers.BokehAppWebsocketConsumer, websocket_urlpatterns)
