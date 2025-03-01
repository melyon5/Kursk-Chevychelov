from flask import Flask

app = Flask(__name__)


@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Варианты выбора</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
  </head>
  <body class="bg-light">
    <div class="container mt-4">
      <h1>Мое предложение: {planet_name}</h1>
      <h2 class="p-2" style="background-color: #C8E6C9;">Эта планета близка к Земле</h2>
      <h2 class="p-2" style="background-color: #A5D6A7;">На ней много необходимых ресурсов</h2>
      <h2 class="p-2" style="background-color: #80DEEA;">На ней есть вода и атмосфера</h2>
      <h2 class="p-2" style="background-color: #FFF59D;">На ней есть небольшое магнитное поле</h2>
      <h2 class="p-2" style="background-color: #FFCDD2;">Наконец, она просто красива!</h2>
    </div>
  </body>
</html>"""


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
