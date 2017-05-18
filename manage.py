"""
Usage: 
    manage.py start (--development | --production) [--host=<host>] [--port=<port>]

Examples:
    python manage.py start --production --host=localhost --port=8080
"""
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
    application.socket_io.run(app, host=arguments["--host"], port=arguments["--port"])
