from flask import Flask, request, jsonify

app = Flask(__name__)

# Главная страница API с HTML описанием
@app.route('/', methods=['GET'])
def get_info():
    html_content = """
    <html>
        <head>
            <title>HOTEL API</title>
        </head>
        <body>
            <h1>Привет, это HOTEL API</h1>
            <p>Наши методы:</p>
            <ul>
                <li><a href="/api/calculate_price_info">/api/calculate_price_info</a> - Получить информацию о расчёте стоимости.</li>
                <li><a href="/api/calculate_price">/api/calculate_price</a> - Рассчитать стоимость проживания.</li>
            </ul>
        </body>
    </html>
    """
    return html_content
    
# GET метод для получения информации о расчёте
@app.route('/api/calculate_price_info', methods=['GET'])
def get_calculation_info():
    return jsonify({
        "description": "Calculates the total price of a stay with discounts, taxes, and fees.",
        "parameters": {
            "base_price": "Base price per night (float)",
            "discount_rate": "Discount percentage (float)",
            "tax_rate": "Tax percentage (float)",
            "service_fee": "Fixed service fee (float)",
            "number_of_nights": "Number of nights (integer)"
        }
    })

# POST метод для расчёта стоимости проживания
@app.route('/api/calculate_price', methods=['POST'])
def calculate_price():
    try:
        data = request.json
        base_price = data.get('base_price')
        discount_rate = data.get('discount_rate')
        tax_rate = data.get('tax_rate')
        service_fee = data.get('service_fee')
        number_of_nights = data.get('number_of_nights')

        # Проверяем, что все данные переданы
        if None in (base_price, discount_rate, tax_rate, service_fee, number_of_nights):
            return jsonify({"error": "Missing required parameters"}), 400

        # Проверяем корректность типов данных
        if not all(isinstance(x, (int, float)) for x in [base_price, discount_rate, tax_rate, service_fee]) or not isinstance(number_of_nights, int):
            return jsonify({"error": "Invalid parameter types"}), 400

        cost_before_discount = base_price * number_of_nights
        discount_amount = cost_before_discount * (discount_rate / 100)
        cost_after_discount = cost_before_discount - discount_amount
        tax_amount = cost_after_discount * (tax_rate / 100)
        total_price = cost_after_discount + tax_amount + service_fee

        return jsonify({"total_price": round(total_price, 2)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80, debug=True)  # Замените '0.0.0.0' на желаемый IP-адрес
