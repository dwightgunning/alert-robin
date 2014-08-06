import cherrypy, logging, logging_conf, json
from logging import config
from alertrobin import AlertRobinService

logging.config.dictConfig(logging_conf.LOGGING)

app_conf = {
    '/order_creation': {
         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
         'tools.response_headers.on': True,
         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
     }
 }

cherrypy.config.update('local_server.conf')
cherrypy.config.update(app_conf)


if __name__=='__main__':
    # Run the application using CherryPy's HTTP Web Server
    app = cherrypy.tree.mount(AlertRobinService(), '/', 'local_app.conf')
    app.merge(app_conf)

    if hasattr(cherrypy.engine, "signal_handler"):
        cherrypy.engine.signal_handler.subscribe()
    if hasattr(cherrypy.engine, "console_control_handler"):
        cherrypy.engine.console_control_handler.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
