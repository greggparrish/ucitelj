from app import app
from livereload import Server


app.DEBUG = True
app.jinja_env.auto_reload = True
server = Server(app.wsgi_app)
server.serve()
