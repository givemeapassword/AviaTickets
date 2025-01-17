from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask import redirect, url_for, session
import logging

# Инициализация базы данных
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Обработчик для страницы не найдена (404)
    @app.errorhandler(404)
    def page_not_found(e):
        session['message'] = "Страница не найдена. Это может быть связано с тем, что страница еще в разработке."
        return redirect(url_for('main.index'))  # Редирект на главную страницу
    
    @app.errorhandler(405)
    def page_not_found(e):
        session['message'] = "Страница не найдена. Это может быть связано с тем, что страница еще в разработке."
        return redirect(url_for('main.index'))  # Редирект на главную страницу

    # Обработчик для серверных ошибок (500)
    @app.errorhandler(500)
    def internal_server_error(e):
        session['message'] = "Что-то пошло не так. Пожалуйста, попробуйте позже."
        return redirect(url_for('main.index'))  # Редирект на главную страницу

    # Настройка логирования
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Инициализация базы данных и миграции
    db.init_app(app)
    migrate.init_app(app, db)

    # Импортируем маршруты
    from app.routes import main_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
