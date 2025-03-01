from flask import Flask, url_for

app = Flask(__name__)

@app.route('/carousel')
def carousel():
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Пейзажи Марса</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
  </head>
  <body>
    <div class="container mt-4">
      <h1 class="text-center">Пейзажи Марса</h1>
      <div id="marsCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="{url_for('static', filename='img/mars1.png')}" class="d-block w-100" alt="Mars1">
          </div>
          <div class="carousel-item">
            <img src="{url_for('static', filename='img/mars2.png')}" class="d-block w-100" alt="Mars2">
          </div>
          <div class="carousel-item">
            <img src="{url_for('static', filename='img/mars3.png')}" class="d-block w-100" alt="Mars3">
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#marsCarousel" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#marsCarousel" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
        </button>
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
