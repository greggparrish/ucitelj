from app import app
from livereload import Server

app.jinja_env.auto_reload = True
server = Server(app.wsgi_app)
server.serve()
