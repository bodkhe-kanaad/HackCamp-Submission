from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

# Import blueprints
from backend.Pairing.routes.pair_routes import pair_bp
from backend.Pairing.routes.pairing_routes import pairing_bp
from backend.Pairing.routes.unpair_routes import unpair_bp
from backend.LeetcodeQuestionService.routes.question_routes import question_bp
from backend.Leaderboard.routes.leaderboard_routes import leaderboard_bp
from backend.Authentication.routes.auth_routes import auth_bp

# Import scheduled task
from backend.Leaderboard.leaderboard_service import update_streaks_for_all_pairs


def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(pair_bp)
    app.register_blueprint(pairing_bp)
    app.register_blueprint(unpair_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(auth_bp)

    # Background scheduler for daily streak reset
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=update_streaks_for_all_pairs,
        trigger="cron",
        hour=0,
        minute=0
    )
    scheduler.start()

    return app


app = create_app()

if __name__ == "__main__":
    # Important: disable reloader or scheduler runs twice
    app.run(debug=True, use_reloader=False)