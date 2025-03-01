from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def mission():
    return "Миссия Колонизация Марса"

@app.route('/index')
def motto():
    return "И на Марсе будут яблони цвести!"

@app.route('/promotion')
def promotion():
    return (
        "Человечество вырастает из детства.<br>"
        "Человечеству мала одна планета.<br>"
        "Мы сделаем обитаемыми безжизненные пока планеты.<br>"
        "И начнем с Марса!<br>"
        "Присоединяйся!"
    )

@app.route('/static/img/mars.png')
def mars_image():
    return send_from_directory('static/img', 'mars.png')

@app.route('/promotion_image')
def promotion_image():
    return """<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Колонизация</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
      body { text-align: center; }
      h1 { color: red; font-size: 36px; margin-top: 20px; }
      img { max-width: 150px; display: block; margin: 0 auto 20px; }
      .container { max-width: 900px; margin: auto; }
      .text-block { font-size: 20px; font-weight: bold; padding: 10px; text-align: center; }
      .gray { background-color: lightgray; }
      .green { background-color: lightgreen; }
      .blue { background-color: lightblue; }
      .yellow { background-color: lightyellow; }
      .pink { background-color: pink; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Жди нас, Марс!</h1>
      <img src="/static/img/mars.png" alt="Марс">
      <div class="text-block gray">Человечество вырастает из детства.</div>
      <div class="text-block green">Человечеству мала одна планета.</div>
      <div class="text-block blue">Мы сделаем обитаемыми безжизненные пока планеты.</div>
      <div class="text-block yellow">И начнем с Марса!</div>
      <div class="text-block pink">Присоединяйся!</div>
    </div>
  </body>
</html>"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
