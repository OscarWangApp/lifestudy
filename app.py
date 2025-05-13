from flask import Flask
from controllers.home_controller import home_bp
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp
from config import Config
from models.database import init_achievement_info, init_total_completed_column, update_user_info_structure, init_last_time_column

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your-secret-key'  # 請更換為安全的密鑰

# Register blueprints
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

# 初始化數據庫
with app.app_context():
    init_achievement_info()
    init_total_completed_column()
    init_last_time_column()
    update_user_info_structure()

if __name__ == '__main__':
    app.run(debug=True)
