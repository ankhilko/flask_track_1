from flask import Flask, render_template, request, redirect
import urllib.parse

app = Flask(__name__)

DEFAULT_CITY = "Минск"
DEFAULT_STREET = "ул. Лобанка"
DEFAULT_HOUSE = "д.77"
DEFAULT_ENTRANCE = "1"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем начальную точку
        start_city = request.form.get('start-city', DEFAULT_CITY).strip()
        start_street = request.form.get('start-street', DEFAULT_STREET).strip()
        start_house = request.form.get('start-house', DEFAULT_HOUSE).strip()
        start_entrance = request.form.get('start-entrance', DEFAULT_ENTRANCE).strip()

        # Формируем полный адрес начальной точки
        start_point = f"{start_city}, {start_street}, {start_house}"
        if start_entrance:
            start_point += f", пд. {start_entrance}"

        # Получаем точки маршрута
        addresses = []
        for i in range(1, 11):
            city = request.form.get(f'point-city-{i}', '').strip()
            street = request.form.get(f'point-street-{i}', '').strip()
            house = request.form.get(f'point-house-{i}', '').strip()
            entrance = request.form.get(f'point-entrance-{i}', DEFAULT_ENTRANCE).strip()

            if city and street and house:
                address = f"{city}, {street}, {house}"
                if entrance:
                    address += f", пд. {entrance}"
                addresses.append(address)

        if len(addresses) < 1:
            return render_template('index.html',
                                   error="Нужна хотя бы одна точка маршрута",
                                   form_data=request.form)

        # Формируем URL для Яндекс.Карт
        yandex_maps_url = generate_yandex_maps_route(start_point, addresses)
        return redirect(yandex_maps_url)

    return render_template('index.html', form_data={})


def generate_yandex_maps_route(start_point, addresses):
    base_url = "https://yandex.ru/maps/?rtext="
    encoded_points = [urllib.parse.quote_plus(start_point)]
    encoded_points += [urllib.parse.quote_plus(point) for point in addresses]
    return base_url + "~".join(encoded_points) + "&rtt=auto"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
