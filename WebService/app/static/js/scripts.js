$(document).ready(function () {
    // Универсальная функция отправки данных на сервер
    const sendCalculationRequest = (url, data, successCallback, errorCallback) => {
        $.ajax({
            url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: successCallback,
            error: errorCallback,
        });
    };

    // Универсальная функция отображения модального окна
    const showModal = (modalId) => {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    };

    const updateCostResults = (response) => {
        console.log("Ответ от сервера:", response);  // Логируем ответ
    
        if (response && response.total_cost && response.breakdown) {
            $('#results').removeClass('d-none');
            $('#total-cost').text(response.total_cost.toFixed(2)); // Общая стоимость
            const mapping = {
                accommodation: 'accommodation-cost',
                flight: 'flight-cost',
                food: 'food-cost',
                transport: 'transport-cost',
                activities: 'activities-cost',
                discount: 'discount',
            };
            console.log("Разбивка стоимости:", response.breakdown);
        
            Object.entries(response.breakdown).forEach(([key, value]) => {
                const elementId = `#${mapping[key] || key}`;
                $(elementId).text(value.toFixed(2) || value);
            });
        } else {
            alert("Ошибка: Неверный формат ответа от API.");
        }
    };
    // Обработчик отправки формы расчета стоимости поездки
    $('#trip-form').submit(function (event) {
        event.preventDefault();
        const formData = {
            country: $('#country').val(),
            season: $('#season').val(),
            duration: +$('#duration').val(),
            num_people: +$('#num_people').val(),
            additional_expenses: +$('#additional_expenses').val(),
        };

        sendCalculationRequest(
            '/api/calculate_trip_cost',
            formData,
            (response) => {
                updateCostResults(response);
                $('#accommodation-form-section').removeClass('d-none');
            },
            (xhr) => alert(`Ошибка: ${xhr.responseJSON?.error || "Неизвестная ошибка"}`)
        );
    });

    // Индивидуальные обработчики кнопок
    $('#buy-ticket').click(function () {
        showModal('ticketModal'); // Модальное окно для покупки билета
    });

    $('#ticketModal .btn-primary, #ticketModal2 .btn-primary').click(function () {
        window.location.href = '/';  // Перенаправление на главную страницу
    });

    $('#buy-ticket2').click(function () {
        showModal('ticketModal2'); // Модальное окно для бронирования отеля
    });

    // Обработчик кнопки "Подробнее"
    $('.btn-details').click(function () {
        const detailsHtml = `
            <h5>${$(this).data('title')}</h5>
            <p>${$(this).data('description')}</p>
            <p><strong>${$(this).data('duration')}</strong></p>
            <p><strong>${$(this).data('price')}</strong></p>
        `;
        $('#detailsModal .modal-body').html(detailsHtml);
        showModal('detailsModal');
    });

    // Закрытие модального окна и возврат на главную страницу
    $('#closeModalBtn').click(() => (window.location.href = '/'));

    // Загрузка курсов валют
    const loadExchangeRates = () => {
        fetch("https://api.exchangerate-api.com/v4/latest/RUB")
            .then((response) => response.json())
            .then((data) => {
                if (data?.rates) {
                    $("#usd-rate").text(`${(1 / data.rates.USD).toFixed(1)} USD`);
                    $("#eur-rate").text(`${(1 / data.rates.EUR).toFixed(1)} EUR`);
                    $("#jpy-rate").text(`${(1 / data.rates.JPY).toFixed(1)} JPY`);
                }
            })
            .catch(() => {
                $(".card-text").text("Не удалось загрузить данные");
                console.error("Ошибка загрузки данных курса валют");
            });
    };

    loadExchangeRates();

    // Обработчик отправки формы расчета стоимости проживания
    $('#accommodation-form').submit(function (event) {
        event.preventDefault();
        const formData = {
            base_price: +$('#base_price').val(),
            discount_rate: +$('#discount_rate').val(),
            tax_rate: +$('#tax_rate').val(),
            service_fee: +$('#service_fee').val(),
            number_of_nights: +$('#number_of_nights').val(),
        };

        sendCalculationRequest(
            '/api/calculate_price', // Новый URL, который обрабатывается Flask
            formData,
            (response) => {
                if (response && response.total_price) {
                    const totalCost = response.total_price.toFixed(2);
                    $('#hotel-results').removeClass('d-none');
                    $('#total-hotel-cost').text(totalCost);
                    $('#total-hotel-cost-all').text((+totalCost + +$('#total-cost').text()).toFixed(2));
                } else {
                    alert("Ошибка: Неверный формат ответа от API.");
                }
            },
            (xhr) => {
                const errorMsg = xhr.responseJSON?.error || "Произошла ошибка при расчете стоимости!";
                alert(`Ошибка: ${errorMsg}`);
            }
        );
    });
});
