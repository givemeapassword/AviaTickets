from flask import Flask, request, jsonify, render_template_string
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app, template_file='swagger.yml')

# Базовые данные
DISCOUNT_PERCENTAGE = 0.1  # 10% скидки за каждого человека, начиная с 3-го
MAX_DISCOUNT = 0.4  # Максимальная скидка - 40% от стоимости
BASE_COST = {
    "USA": {"flight": 600, "accommodation": 150, "food": 30, "transport": 20},
    "France": {"flight": 500, "accommodation": 200, "food": 25, "transport": 15},
    "Japan": {"flight": 800, "accommodation": 250, "food": 35, "transport": 25}
}

SEASONAL_FACTORS = {
    "summer": 1.2,
    "winter": 1.5,
    "offseason": 1.0
}

# Главная страница API с HTML описанием
@app.route('/', methods=['GET'])
def get_info():
    html_content = """
    <html>
        <head>
            <title>TRAVEL API</title>
        </head>
        <body>
            <h1>Привет, это TRAVEL API</h1>
            <p>Наши методы:</p>
            <ul>
                <li><a href="/api/calculate_trip_cost">/api/calculate_trip_cost</a> - Рассчитать стоимость путешествия.</li>
                <li><a href="/api/get_trip_cost_info">/api/get_trip_cost_info</a> - Получить информацию о стоимости для выбранной страны и сезона.</li>
            </ul>
        </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/api/calculate_trip_cost', methods=['POST'])
def calculate_trip_cost():
    data = request.json
    try:
        # Извлечение и валидация параметров
        country = data['country']
        season = data['season']
        duration = int(data['duration'])
        additional_expenses = float(data['additional_expenses'])
        num_people = int(data['num_people'])

        if country not in BASE_COST or season not in SEASONAL_FACTORS:
            return jsonify({"error": "Неверная страна или сезон"}), 400

        # Расчет стоимости
        base = BASE_COST[country]
        seasonal_multiplier = SEASONAL_FACTORS[season]

        flight_cost = base["flight"] * seasonal_multiplier * num_people
        accommodation_cost = base["accommodation"] * duration * num_people
        food_cost = base["food"] * duration * num_people
        transport_cost = base["transport"] * duration * num_people

        total = flight_cost + accommodation_cost + food_cost + transport_cost + additional_expenses

        # Логика скидки
        if num_people > 2:
            # Скидка начинается с 3-го человека
            discount_percentage = (num_people - 2) * DISCOUNT_PERCENTAGE
            # Ограничение скидки до 40%
            discount_percentage = min(discount_percentage, MAX_DISCOUNT)
        else:
            discount_percentage = 0  # Нет скидки для 2 или меньше человек
        # Скидка
        discount_amount = total * discount_percentage  # Рассчитываем скидку от общей стоимости
        total_cost = total - discount_amount  # Итоговая стоимость после скидки

        return jsonify({
            "total_cost": round(total_cost, 2),
            "breakdown": {
                "flight": round(flight_cost, 2),
                "accommodation": round(accommodation_cost, 2),
                "food": round(food_cost, 2),
                "transport": round(transport_cost, 2),
                "activities": round(additional_expenses, 2),
                "discount": round(discount_percentage*100, 2)
            }
        })
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Некорректные данные"}), 400


@app.route('/api/get_trip_cost_info', methods=['GET'])
def get_trip_cost_info():
    country = request.args.get('country')
    season = request.args.get('season')

    if country not in BASE_COST or season not in SEASONAL_FACTORS:
        return jsonify({"error": "Неверная страна или сезон"}), 400

    base = BASE_COST[country]
    seasonal_multiplier = SEASONAL_FACTORS[season]

    return jsonify({
        "country": country,
        "season": season,
        "flight_cost": round(base["flight"] * seasonal_multiplier, 2),
        "accommodation_cost": round(base["accommodation"], 2),
        "food_cost": round(base["food"], 2),
        "transport_cost": round(base["transport"], 2)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
