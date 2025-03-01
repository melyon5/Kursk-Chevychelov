import os
from flask import Flask, request, url_for

app = Flask(__name__)

@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    saved_filename = 'uploaded_photo.png'
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file.save(os.path.join('static', 'img', saved_filename))
    return f"""<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Отбор астронавтов</title>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{url_for('static', filename='css/style.css')}">
  </head>
  <body>
    <div class="container mt-4">
      <h1 class="text-center">Загрузка фотографии</h1>
      <h3 class="text-center">для участия в миссии</h3>
      <div class="card p-3 bg-light" id="upload-card">
        <form method="POST" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="photo" class="form-label">Приложите фотографию</label>
            <input type="file" class="form-control" id="photo" name="file">
          </div>
          <button type="submit" class="btn btn-primary">Отправить</button>
        </form>
      </div>
      <div class="text-center mt-4">
        <img src="{url_for('static', filename='img/' + saved_filename)}"
             alt="Загруженное фото"
             class="img-fluid"
             style="max-height: 300px;">
      </div>
    </div>
  </body>
</html>"""

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
