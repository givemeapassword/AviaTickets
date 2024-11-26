$(document).ready(function() {
    // Функция для отправки данных на сервер
    function sendCalculationRequest(url, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: successCallback,
            error: errorCallback
        });
    }

    // Функция для обновления результатов расчета стоимости
    function updateCostResults(response) {
        $('#results').removeClass('d-none');
        $('#total-cost').text(response.total_cost);
        $('#flight-cost').text(response.breakdown.flight);
        $('#accommodation-cost').text(response.breakdown.accommodation);
        $('#food-cost').text(response.breakdown.food);
        $('#transport-cost').text(response.breakdown.transport);
        $('#activities-cost').text(response.breakdown.activities);
        $('#discount').text(response.breakdown.discount);
    }

    // Функция для отображения модального окна
    function showModal(modalId) {
        var myModal = new bootstrap.Modal(document.getElementById(modalId));
        myModal.show();
    }

    // Обработчик отправки формы для расчета стоимости
    $('#trip-form').submit(function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы

        const formData = {
            country: $('#country').val(),
            season: $('#season').val(),
            duration: $('#duration').val(),
            num_people: $('#num_people').val(),
            additional_expenses: $('#additional_expenses').val()
        };

        sendCalculationRequest('/api/calculate_trip_cost', formData, function(response) {
            updateCostResults(response);
            $('#accommodation-form-section').removeClass('d-none');
        }, function(xhr) {
            alert("Ошибка: " + xhr.responseJSON.error);
        });
    });

    // Обработчик для кнопки "Хотите купить билет?"
    $('#buy-ticket').click(function() {
        // Открываем модальное окно с сообщением о покупке билета
        showModal('ticketModal');
    });

    // Обработчик для кнопки "Хотите купить билет?" (другая кнопка)
    $('#buy-ticket2').click(function() {
        showModal('ticketModal2');
    });

    // Обработчик для кнопки "Подробнее" (модальное окно с деталями)
    $('.btn-details').click(function() {
        const title = $(this).data('title');
        const description = $(this).data('description');
        const duration = $(this).data('duration');
        const price = $(this).data('price');

        const detailsHtml = `
            <h5>${title}</h5>
            <p>${description}</p>
            <p><strong>${duration}</strong></p>
            <p><strong>${price}</strong></p>
        `;
        $('#detailsModal .modal-body').html(detailsHtml);
        showModal('detailsModal');
    });

    // Закрытие модального окна с возвратом на главную страницу
    $('#closeModalBtn').click(function() {
        window.location.href = '/';
    });

    // Загрузка курсов валют при загрузке страницы
    function loadExchangeRates() {
        const apiUrl = "https://api.exchangerate-api.com/v4/latest/RUB";

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data && data.rates) {
                    const rates = data.rates;
                    $("#usd-rate").text(`${(1 / rates["USD"]).toFixed(1)} USD`);
                    $("#eur-rate").text(`${(1 / rates["EUR"]).toFixed(1)} EUR`);
                    $("#jpy-rate").text(`${(1 / rates["JPY"]).toFixed(1)} JPY`);
                }
            })
            .catch(error => {
                console.error("Ошибка загрузки данных курса валют:", error);
                $(".card-text").text("Не удалось загрузить данные");
            });
    }

    loadExchangeRates();  // Вызываем функцию для загрузки данных курса валют

    $('#accommodation-form').submit(function(event) {
        event.preventDefault(); // предотвращаем стандартное поведение формы
    
        const formData = {
            base_price: $('#base_price').val(),        // Название поля должно совпадать с ожиданием API
            discount_rate: $('#discount_rate').val(),
            tax_rate: $('#tax_rate').val(),
            service_fee: $('#service_fee').val(),
            number_of_nights: $('#number_of_nights').val()
        };
    
        // Отправляем запрос на сервер
        sendCalculationRequest('http://127.0.0.1:5000/api/calculate_price', formData, function(response) {
            $('#hotel-results').removeClass('d-none');
            $('#total-hotel-cost').text(response.total_price.toFixed(2)); // Используем поле "total_price" из ответа
            $('#total-hotel-cost-all').text((response.total_price + parseFloat($('#total-cost').text())).toFixed(2));
        }, function(xhr) {
            // Обработка ошибок
            if (xhr.responseJSON && xhr.responseJSON.error) {
                alert("Ошибка: " + xhr.responseJSON.error);
            } else {
                alert("Произошла ошибка при расчете стоимости!");
            }
        });
    });
    
    // Функция для отправки AJAX-запроса
    function sendCalculationRequest(url, data, successCallback, errorCallback) {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: successCallback,
            error: errorCallback
        });
    }
    

});
