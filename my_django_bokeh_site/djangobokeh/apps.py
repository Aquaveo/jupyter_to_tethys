import os
import glob

from django.apps import AppConfig
from django.conf import settings

from bokeh.command.util import build_single_handler_application
from bokeh.server.contexts import ApplicationContext
from bokeh.server.urls import per_app_patterns, toplevel_patterns
from bokeh.application.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.application.handlers.document_lifecycle import DocumentLifecycleHandler


class DjangoBokehConfig(AppConfig):

    name = 'djangobokeh'

    def ready(self):

        print("DjangoBokehConfig.ready()")
        os.environ['BOKEH_NODEJS_PATH'] = settings.BOKEH_NODEJS_PATH

        bokeh_app_base_path = os.path.join(settings.BASE_DIR, "djangobokeh", "bokeh_apps")
        path_list = glob.glob(os.path.join(bokeh_app_base_path, "*.py"))
        print(path_list)

        applications = {}
        for path in path_list:
            application = build_single_handler_application(path)

            route = application.handlers[0].url_path()

            if not route:
                if '/' in applications:
                    raise RuntimeError("Don't know the URL path to use for %s" % (path))
                route = '/'
            applications[route] = application

        if callable(applications):
            applications = Application(FunctionHandler(applications))

        if isinstance(applications, Application):
            applications = {'/': applications}

        for k, v in list(applications.items()):
            if callable(v):
                applications[k] = Application(FunctionHandler(v))
            if all(not isinstance(handler, DocumentLifecycleHandler)
                   for handler in applications[k]._handlers):
                applications[k].add(DocumentLifecycleHandler())

        self._applications = dict()
        for k, v in applications.items():
            self._applications[k] = ApplicationContext(v, url=k)

        prefix = None
        if prefix is None:
            prefix = ""
        prefix = prefix.strip("/")
        if prefix:
            prefix = "/" + prefix

        self._prefix = prefix
        extra_patterns = None
        extra_patterns = extra_patterns or []
        self.all_patterns = []
        for key, app in applications.items():
            app_patterns = []
            for p in per_app_patterns:
                if key == "/":
                    route = p[0]
                else:
                    route = key + p[0]
                route = self._prefix + route
                app_patterns.append((route, p[1], {"application_context": self._applications[key]}))

            websocket_path = None
            for r in app_patterns:
                if r[0].endswith("/ws"):
                    websocket_path = r[0]
            if not websocket_path:
                raise RuntimeError("Couldn't find websocket path")
            for r in app_patterns:
                r[2]["bokeh_websocket_path"] = websocket_path

            self.all_patterns.extend(app_patterns)
