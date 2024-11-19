$(document).ready(function() {
    // Обработчик отправки формы для расчета стоимости
    $('#trip-form').submit(function(event) {
        event.preventDefault();  // предотвращаем стандартное поведение формы

        // Получаем данные из формы
        const country = $('#country').val();
        const season = $('#season').val();
        const duration = $('#duration').val();
        const num_people = $('#num_people').val();
        const additional_expenses = $('#additional_expenses').val();

        // Отправляем данные на сервер
        $.ajax({
            url: '/api/calculate_trip_cost',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                country: country,
                season: season,
                duration: duration,
                num_people: num_people,
                additional_expenses: additional_expenses
            }),
            success: function(response) {
                // Когда расчет успешен, показываем результаты
                $('#results').removeClass('d-none');  // показываем блок результатов
                $('#total-cost').text(response.total_cost);
                $('#flight-cost').text(response.breakdown.flight);
                $('#accommodation-cost').text(response.breakdown.accommodation);
                $('#food-cost').text(response.breakdown.food);
                $('#transport-cost').text(response.breakdown.transport);
                $('#activities-cost').text(response.breakdown.activities);
                $('#discount').text(response.breakdown.discount);
            },
            error: function(xhr) {
                // Показываем сообщение об ошибке
                alert("Ошибка: " + xhr.responseJSON.error);
            }
        });
    });

    // Обработчик для кнопки "Хотите купить билет?"
    $('#buy-ticket').click(function() {
        // Открываем модальное окно с сообщением о покупке билета
        var myModal = new bootstrap.Modal(document.getElementById('ticketModal'));
        myModal.show();
    });
});


$(document).ready(function() {
    // Обработчик отправки формы для расчета стоимости
    $('#trip-form').on('submit', function(e) {
        e.preventDefault();

        const country = $('#country').val();
        const season = $('#season').val();
        const duration = $('#duration').val();
        const num_people = $('#num_people').val();
        const additional_expenses = $('#additional_expenses').val();

        // Отправка данных на сервер для расчета стоимости
        $.ajax({
            url: '/api/calculate_trip_cost',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                country: country,
                season: season,
                duration: duration,
                num_people: num_people,
                additional_expenses: additional_expenses
            }),
            success: function(response) {
                // Отображаем результаты на странице
                $('#results').removeClass('d-none');
                $('#total-cost').text(response.total_cost);
                $('#flight-cost').text(response.breakdown.flight);
                $('#accommodation-cost').text(response.breakdown.accommodation);
                $('#food-cost').text(response.breakdown.food);
                $('#transport-cost').text(response.breakdown.transport);
                $('#activities-cost').text(response.breakdown.activities);
                $('#discount').text(response.breakdown.discount);
            },
            error: function(error) {
                alert('Произошла ошибка при расчете стоимости!');
            }
        });
    });

    $('.btn-details').on('click', function () {
        const title = $(this).data('title');
        const description = $(this).data('description');
        const duration = $(this).data('duration');
        const price = $(this).data('price');

        // Формируем HTML для отображения информации
        const detailsHtml = `
            <h5>${title}</h5>
            <p>${description}</p>
            <p><strong>${duration}</strong></p>
            <p><strong>${price}</strong></p>
        `;

        // Вставляем данные в модальное окно
        $('#detailsModal .modal-body').html(detailsHtml);

        // Показываем модальное окно
        const detailsModal = new bootstrap.Modal(document.getElementById('detailsModal'));
        detailsModal.show();
    });

});
$(document).ready(function () {
    // Функция для загрузки курсов валют относительно рубля
    function loadExchangeRates() {
        const apiUrl = "https://api.exchangerate-api.com/v4/latest/RUB"; // Замените на ваше API

        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data && data.rates) {
                    const rates = data.rates;

                    // Получение курсов
                    const usdRate = (1 / rates["USD"]).toFixed(1) || "Нет данных";
                    const eurRate = (1 / rates["EUR"]).toFixed(1) || "Нет данных";
                    const jpyRate = (1 / rates["JPY"]).toFixed(1) || "Нет данных";

                    // Обновление карточек
                    $("#usd-rate").text(`${usdRate} USD`);
                    $("#eur-rate").text(`${eurRate} EUR`);
                    $("#jpy-rate").text(`${jpyRate} JPY`);
                }
            })
            .catch(error => {
                console.error("Ошибка загрузки данных курса валют:", error);
                $(".card-text").text("Не удалось загрузить данные");
            });
    }

    // Загрузка данных при загрузке страницы
    loadExchangeRates();
});

$(document).ready(function () {
    // Обработчик для кнопки "Хотите купить билет?"
    $('#buy-ticket').click(function () {
      // Получаем данные из формы
      const country = $('#country').val();
      const season = $('#season').val();
      const duration = $('#duration').val();
      const num_people = $('#num_people').val();
      const additional_expenses = $('#additional_expenses').val();
  
      // Заполняем информацию о выбранной поездке в модальном окне
      $('#selected-country').text(country);
      $('#selected-season').text(season);
      $('#selected-duration').text(duration);
      $('#selected-num-people').text(num_people);
      $('#selected-additional-expenses').text(additional_expenses);
  
      // Генерируем список поездок
      const trips = [
        { name: 'Тур по Барселоне', description: 'Прекрасные виды, отличный климат и культурные достопримечательности.' },
        { name: 'Поездка на Пальму', description: 'Идеальное место для расслабления и наслаждения солнцем.' },
        { name: 'Тур по Мадриду', description: 'Романтика старого города и современные достопримечательности.' }
      ];
  
      // Очистим список поездок
      $('#trip-list').empty();
  
      // Добавляем каждый тур в список
      trips.forEach(trip => {
        $('#trip-list').append(`
          <li class="list-group-item">
            <strong>${trip.name}</strong>
            <p>${trip.description}</p>
          </li>
        `);
      });
  
      // Открываем модальное окно
      var myModal = new bootstrap.Modal(document.getElementById('tripModal'));
      myModal.show();
    });
  });
  

