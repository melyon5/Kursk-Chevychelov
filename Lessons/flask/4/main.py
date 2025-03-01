from flask import Flask, request

app = Flask(__name__)


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    if request.method == 'GET':
        return """<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8">
    <title>Отбор астронавтов</title>
    <link rel="stylesheet" 
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
  </head>
  <body>
    <h1 class="text-center mt-3">Анкета претендента на участие в миссии</h1>
    <div class="container mt-4" style="max-width: 600px;">
      <form method="post" enctype="multipart/form-data">
        <div class="form-group">
          <label for="surname">Фамилия</label>
          <input type="text" class="form-control" id="surname" 
                 placeholder="Введите фамилию" name="surname">
        </div>
        <div class="form-group">
          <label for="name">Имя</label>
          <input type="text" class="form-control" id="name" 
                 placeholder="Введите имя" name="name">
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" class="form-control" id="email" 
                 placeholder="Введите адрес почты" name="email">
        </div>
        <div class="form-group">
          <label for="education">Образование</label>
          <input type="text" class="form-control" id="education"
                 placeholder="Введите ваше образование" name="education">
        </div>
        <div class="form-group">
          <label>Какие у вас профессии?</label>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof1" 
                   name="prof" value="инженер-исследователь">
            <label class="form-check-label" for="prof1">
              Инженер-исследователь
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof2" 
                   name="prof" value="пилот">
            <label class="form-check-label" for="prof2">
              Пилот
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof3" 
                   name="prof" value="строитель">
            <label class="form-check-label" for="prof3">
              Строитель
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof4" 
                   name="prof" value="экзобиолог">
            <label class="form-check-label" for="prof4">
              Экзобиолог
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof5" 
                   name="prof" value="врач">
            <label class="form-check-label" for="prof5">
              Врач
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof6" 
                   name="prof" value="инженер по терраформированию">
            <label class="form-check-label" for="prof6">
              Инженер по терраформированию
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof7" 
                   name="prof" value="климатолог">
            <label class="form-check-label" for="prof7">
              Климатолог
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof8" 
                   name="prof" value="специалист по радиационной защите">
            <label class="form-check-label" for="prof8">
              Специалист по радиационной защите
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof9" 
                   name="prof" value="астрогеолог">
            <label class="form-check-label" for="prof9">
              Астрогеолог
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof10" 
                   name="prof" value="гляциолог">
            <label class="form-check-label" for="prof10">
              Гляциолог
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof11" 
                   name="prof" value="инженер жизнеобеспечения">
            <label class="form-check-label" for="prof11">
              Инженер жизнеобеспечения
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof12" 
                   name="prof" value="метеоролог">
            <label class="form-check-label" for="prof12">
              Метеоролог
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof13" 
                   name="prof" value="оператор марсохода">
            <label class="form-check-label" for="prof13">
              Оператор марсохода
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof14" 
                   name="prof" value="киберинженер">
            <label class="form-check-label" for="prof14">
              Киберинженер
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof15" 
                   name="prof" value="штурман">
            <label class="form-check-label" for="prof15">
              Штурман
            </label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="checkbox" id="prof16" 
                   name="prof" value="пилот дронов">
            <label class="form-check-label" for="prof16">
              Пилот дронов
            </label>
          </div>
        </div>
        <div class="form-group">
          <label>Укажите пол</label>
          <div class="form-check">
            <input class="form-check-input" type="radio" name="sex" 
                   id="male" value="male">
            <label class="form-check-label" for="male">Мужской</label>
          </div>
          <div class="form-check">
            <input class="form-check-input" type="radio" name="sex" 
                   id="female" value="female">
            <label class="form-check-label" for="female">Женский</label>
          </div>
        </div>
        <div class="form-group">
          <label for="motivation">Почему вы хотите принять участие в миссии?</label>
          <textarea class="form-control" id="motivation" 
                    rows="3" name="motivation"></textarea>
        </div>
        <div class="form-group">
          <label for="photo">Приложите фотографию</label>
          <input type="file" class="form-control-file" id="photo" name="photo">
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="mars" name="mars">
          <label class="form-check-label" for="mars">
            Готовы остаться на Марсе?
          </label>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Отправить</button>
      </form>
    </div>
  </body>
</html>"""
    else:
        return "Форма отправлена"


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
