from flask import Flask
from flask_cors import CORS

# --- IMPORT BLUEPRINTS ---
from Authentication.routes.auth_routes import auth_bp
from Pairing.routes.pairing_routes import pair_bp
from Pairing.routes.unpair_routes import unpair_bp
from LeetcodeQuestionService.routes.question_routes import question_bp


def create_app():
    app = Flask(__name__)

    # FIXED CORS (applies to ALL routes, including blueprints)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # ---- REGISTER BLUEPRINTS ----
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(pair_bp, url_prefix="/api")
    app.register_blueprint(unpair_bp, url_prefix="/api")
    app.register_blueprint(question_bp, url_prefix="/api")

    @app.get("/")
    def home():
        return {"message": "Backend running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
