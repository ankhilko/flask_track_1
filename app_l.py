from flask import Flask, render_template, request, redirect
import urllib.parse

app = Flask(__name__)

DEFAULT_START_POINT = "Минск, ул. Лобанка, д.77"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем адреса из формы
        addresses = [
            request.form.get(f'point-{i}', '').strip()
            for i in range(1, 11)
            if request.form.get(f'point-{i}', '').strip()
        ]

        if len(addresses) < 1:  # Минимум 1 точка маршрута
            return render_template('index.html',
                                   error="Нужна хотя бы одна точка маршрута",
                                   start_point=request.form.get('start-point', DEFAULT_START_POINT),
                                   points=request.form)

        # Формируем URL для Яндекс.Карт
        yandex_maps_url = generate_yandex_maps_route(
            start_point=request.form.get('start-point', DEFAULT_START_POINT),
            addresses=addresses
        )
        return redirect(yandex_maps_url)

    # GET запрос - отображаем форму с дефолтными значениями
    return render_template('index.html',
                           start_point=DEFAULT_START_POINT,
                           points={})


def generate_yandex_maps_route(start_point, addresses):
    base_url = "https://yandex.ru/maps/?rtext="

    # Кодируем все точки маршрута
    all_points = [start_point] + addresses
    encoded_points = [
        urllib.parse.quote_plus(point)
        for point in all_points
    ]

    # Формируем параметр rtext в формате: точка1~точка2~точка3
    route_param = "~".join(encoded_points)

    return base_url + route_param + "&rtt=auto"  # rtt=auto - для автомобильного маршрута


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
