# from flask import Flask
# app = Flask(__name__)

# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name

# if __name__ == '__main__':
#    app.run()



from flask import Flask
from flask_cors import CORS

# --- IMPORT BLUEPRINTS ---
# Auth
from Authentication.routes.auth_routes import auth_bp
# Pairing
from Pairing.routes.pairing_routes import pair_bp
from Pairing.routes.unpair_routes import unpair_bp
# LeetCode Questions
from LeetcodeQuestionService.routes.question_routes import question_bp


def create_app():
    app = Flask(__name__)
    CORS(app)  # allow frontend on localhost:5173 to access API

    # ---- REGISTER BLUEPRINTS ----
    # Authentication
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Pairing system
    app.register_blueprint(pair_bp, url_prefix="/api")
    app.register_blueprint(unpair_bp, url_prefix="/api")

    # LeetCode question engine
    app.register_blueprint(question_bp, url_prefix="/api")

    # Test route
    @app.get("/")
    def home():
        return {"message": "Backend running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
