"""
Usage: 
    manage.py start (--development | --production) [--host=<host>] [--port=<port>]

Examples:
    python manage.py start --production --host=localhost --port=8080
"""
import eventlet
eventlet.monkey_patch()

from docopt import docopt

import config
import application

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments["--development"]:
        app = application.create(config.DevelopmentConfig)
    else:
        app = application.create(config.ProductionConfig)
    app.app_context().push()
    application.db.create_all()

    host = arguments["--host"] if arguments["--host"] else "0.0.0.0"
    port = int(arguments["--port"]) if arguments["--port"] else None
    application.socket_io.run(app, host=host, port=port)
