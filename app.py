from flask import Flask
from controllers.home_controller import home_bp
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from controllers.location_controller import location_bp
from controllers.achievement_controller import achievement_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key'  # 請更換為安全的密鑰

# Register blueprints
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(location_bp, url_prefix='/location')
app.register_blueprint(achievement_bp, url_prefix='/achievement')

if __name__ == '__main__':
    app.run(debug=True)
