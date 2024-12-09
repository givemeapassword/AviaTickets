from flask import Blueprint, request, jsonify, render_template, session
from app.models import  Country, SeasonFactor
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

# Главная страница
@main_bp.route('/')
def index():
    countries = Country.query.all()  # Загружаем все страны
    seasons = SeasonFactor.query.all()  # Загружаем все сезоны
    message = session.pop('message', None)  # Получаем и удаляем сообщение из сессии
    return render_template('index.html', message=message, countries=countries, seasons=seasons)


@main_bp.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():
    api_url = "http://travelapi-animeanime111.amvera.io:80/api/calculate_trip_cost"
    data = request.json

    # Проверка обязательных параметров
    required_keys = {'country', 'season', 'duration', 'additional_expenses', 'num_people'}
    if not required_keys.issubset(data):
        logging.error(f"Пропущены обязательные параметры: {required_keys - data.keys()}")
        return jsonify({"error": "Не все обязательные параметры указаны"}), 400

    try:
        # Отправка запроса к API
        logging.debug(f"Отправляемые данные: {data}")
        response = requests.post(api_url, json=data)
        response.raise_for_status()

        # Логируем ответ
        logging.debug(f"Ответ API: {response.status_code}, {response.text}")

        # Передаем ответ на фронт (проверить структуру ответа)
        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return jsonify({"error": "Ошибка соединения с API"}), 500


@main_bp.route('/api/calculate_price', methods=['POST'])
def calculate_price():
    api_url = "http://sam-service-animeanime111.amvera.io/api/calculate_price"
    data = request.json

    # Проверка обязательных параметров
    required_keys = {'base_price', 'discount_rate', 'tax_rate', 'service_fee', 'number_of_nights'}
    if not required_keys.issubset(data):
        missing_keys = required_keys - data.keys()
        logging.error(f"Пропущены обязательные параметры: {missing_keys}")
        return jsonify({"error": f"Не все обязательные параметры указаны: {missing_keys}"}), 400

    try:
        # Отправка запроса к API отелей
        logging.debug(f"Отправляемые данные: {data}")
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        logging.debug(f"Ответ API: {response.status_code}, {response.text}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API отелей: {e}")
        return jsonify({"error": "Ошибка соединения с API"}), 500


@main_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Получаем строку поиска
    countries = (
        Country.query.filter(Country.country_name.ilike(f'%{query}%')).all()
        if query else []
    )
    seasons = (
        SeasonFactor.query.filter(SeasonFactor.season.ilike(f'%{query}%')).all()
        if query else []
    )

    # Возвращаем частичный HTML
    return render_template('search_modal_content.html', query=query, countries=countries, seasons=seasons)
