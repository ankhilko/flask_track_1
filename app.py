from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    # В реальном приложении здесь бы вызывался API Яндекс.Карт для оптимизации маршрута
    # Но так как мы не используем API ключ, просто возвращаем те же точки в другом порядке
    data = request.json
    points = data['points']

    # Простая "оптимизация" - просто меняем порядок точек (кроме первой)
    if len(points) > 2:
        optimized_points = [points[0]] + points[:0:-1]
    else:
        optimized_points = points

    return jsonify({
        'optimized_points': optimized_points,
        'message': 'Маршрут оптимизирован (в демо-режиме просто изменен порядок точек)'
    })


if __name__ == '__main__':
    app.run(debug=True)