from flask import Blueprint, request, jsonify, render_template, session
from app.models import Country, SeasonFactor
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

main_bp = Blueprint('main', __name__)

# Основные API-URL
TRAVEL_API_URL = "http://travelapi-animeanime111.amvera.io:80/api/calculate_trip_cost"
SAM_SERVICE_URL = "http://sam-service-animeanime111.amvera.io/api/calculate_price"

# Локальные API-URL в Docker-сети
TRAVEL_API_LOCAL = "http://travel_api:80/api/calculate_trip_cost"
SAM_SERVICE_LOCAL = "http://hotel_api:80/api/calculate_price"

def check_api_availability(url):
    """Проверяет доступность API"""
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Главная страница
@main_bp.route('/')
def index():
    countries = Country.query.all()  # Загружаем все страны
    seasons = SeasonFactor.query.all()  # Загружаем все сезоны
    message = session.pop('message', None)  # Получаем и удаляем сообщение из сессии
    return render_template('index.html', message=message, countries=countries, seasons=seasons)

@main_bp.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():
    data = request.json
    required_keys = {'country', 'season', 'duration', 'additional_expenses', 'num_people'}

    if not required_keys.issubset(data):
        missing_keys = required_keys - data.keys()
        logging.error(f"Пропущены обязательные параметры: {missing_keys}")
        return jsonify({"error": f"Не все обязательные параметры указаны: {missing_keys}"}), 400

    # Проверяем доступность API
    api_url = TRAVEL_API_URL if check_api_availability(TRAVEL_API_URL) else TRAVEL_API_LOCAL
    logging.info(f"Используем API: {api_url}")

    try:
        logging.debug(f"Отправляемые данные: {data}")
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        logging.debug(f"Ответ API: {response.status_code}, {response.text}")
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при запросе к API: {e}")
        return jsonify({"error": "Ошибка соединения с API"}), 500

@main_bp.route('/api/calculate_price', methods=['POST'])
def calculate_price():
    data = request.json
    required_keys = {'base_price', 'discount_rate', 'tax_rate', 'service_fee', 'number_of_nights'}

    if not required_keys.issubset(data):
        missing_keys = required_keys - data.keys()
        logging.error(f"Пропущены обязательные параметры: {missing_keys}")
        return jsonify({"error": f"Не все обязательные параметры указаны: {missing_keys}"}), 400

    # Проверяем доступность API
    api_url = SAM_SERVICE_URL if check_api_availability(SAM_SERVICE_URL) else SAM_SERVICE_LOCAL
    logging.info(f"Используем API: {api_url}")

    try:
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
