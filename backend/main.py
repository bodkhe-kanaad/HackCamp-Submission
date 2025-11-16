from flask import Flask
from Authentication.routes.auth_routes import auth_bp

app = Flask(__name__)

# Register the auth blueprint
app.register_blueprint(auth_bp)

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

if __name__ == '__main__':
   app.run()