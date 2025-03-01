from flask import Flask

app = Flask(__name__)

@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Результаты</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
  </head>
  <body>
    <div class="container mt-4">
      <h1>Результаты отбора</h1>
      <h2>Претендента на участие в миссии {nickname}:</h2>
      <div class="p-3 mb-2" style="background-color: #C8E6C9;">
        <h3>Поздравляем! Ваш рейтинг после {level} этапа отбора</h3>
        <h3>составляет {rating}!</h3>
      </div>
      <div class="p-3 mb-2" style="background-color: #FFF9C4;">
        <h3>Желаем удачи!</h3>
      </div>
    </div>
  </body>
</html>"""

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
