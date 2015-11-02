# Set the path
import os
import RaspApp
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server
from werkzeug.contrib.fixers import ProxyFix

from RaspApp import app


app.wgsi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    threaded=True,
    host='0.0.0.0')
)

#RaspApp.add_routes(app)

if __name__ == "__main__":
    manager.run()
