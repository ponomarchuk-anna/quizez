from collections import Counter
from forms import LoginForm, RegForm, QuizForm
from model import db, Answer, Quiz, User
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    user_id = request.args.get('user_id')
    if user_id:
        title = 'Мои квизы'
        quizes = Quiz.query.filter(Quiz.user_id == user_id).all()
    else:
        title = 'Квизы'
        quizes = Quiz.query.all()
    return render_template(
        'index.html',
        title=title,
        quizes=quizes,
    )


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Авторизация'
    form = LoginForm()
    return render_template(
        'login.html',
        title=title,
        form=form,
    )


@app.route('/login-process', methods=['POST'])
def login_process():
    form = LoginForm()
    user = User.query.filter(User.username == form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('С возвращением!')
        return redirect(url_for('index'))
    flash('Проверьте корректность имени пользователя и пароля!')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    logout_user()
    flash('До свидания!')
    return redirect(url_for('index'))


@app.route('/reg')
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Регистрация'
    form = RegForm()
    return render_template(
        'reg.html',
        title=title,
        form=form,
    )


@app.route('/reg-process', methods=['POST'])
def reg_process():
    form = RegForm()
    if form.validate_on_submit():
        check_user = User.query.filter(User.username == form.username.data).count()
        if not check_user:
            new_user = User(username=form.username.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('login'))
        flash('Данное имя пользователя уже занято')
    flash('Пароли не совпадают!')
    return redirect(url_for('reg'))


@app.route('/add_quiz', methods=['POST', 'GET'])
def add_quiz():
    if current_user.is_authenticated:
        form = QuizForm()
        title = 'Создание квиза'
        if request.method == 'GET':
            form = QuizForm()
            return render_template(
                'add_quiz.html',
                title=title,
                form=form,
            )
        else:
            session['counter'] = int(form.counter.data)
            session['name'] = form.name.data
            if len(form.access.data) > 0:
                session['access'] = form.access.data.split(';')
            else:
                session['access'] = []
            # проверка уникальности имени квиза
            return render_template(
                'add_quiz.html',
                title=title,
                form=form,
                counter=session['counter'],
            )
    return redirect(url_for('login'))


@app.route('/save-quiz', methods=['post'])
def save_quiz():
    questions = request.form
    res = {}
    print(len(questions))
    for i in range(1, session['counter'] + 1):
        quest = questions[f'q{i}'].strip().capitalize()
        answers = questions[f'a{i}'].split(';')
        req = questions.get(f'r{i}', 'off')
        many = questions.get(f'm{i}', 'off')
        answers = [req, many] + [a.strip().capitalize() for a in answers]
        res[quest] = answers
    new_quiz = Quiz(
        name=session['name'],
        data=res,
        access=session['access'],
        user_id=current_user.id,
        )
    db.session.add(new_quiz)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/quiz/<int:quiz_id>')
def show_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz.access or current_user.username in quiz.access or current_user.id == quiz.user_id:
        return render_template(
            'quiz.html', quiz=quiz,
            )
    flash('У вас нет доступа к этому опросу :(')
    return redirect(url_for('index'))


@app.route('/save-answers', methods=['post'])
def save_answers():
    quiz_id = request.referrer.split('/')[-1]
    res = {}
    for k, v in request.form.items():
        if k[-1].isdigit():
            k = '_'.join(k.split('_')[:-1])
        k = k.replace('_', ' ')
        res.setdefault(k, [])
        res[k].append(v)
    new_answers = Answer(
        answers=res,
        user_id=current_user.id,
        quiz_id=quiz_id,
    )
    db.session.add(new_answers)
    db.session.commit()
    flash('Ваши ответы сохранены!')
    return redirect(url_for('index'))


@app.route('/stats/<int:quiz_id>')
def stats(quiz_id):
    answers = Answer.query.filter(Answer.quiz_id == quiz_id).with_entities(Answer.answers).all()
    res = {}
    for a in answers:
        for k, v in a[0].items():
            res.setdefault(k, [])
            for i in v:
                res[k].append(i)
    res = {k: Counter(v) for k, v in res.items()}

    img = {}
    for k, v in res.items():
        img.setdefault(k, [])
        for k2, v2 in v.items():
            img[k] += [k2] * v2
    for k, v in img.items():
        plt.hist(v).savefig(f'./static/images/{k}.png')
        img[k] = f'/static/images/{k}.png'
    print(img)
    return render_template(
        'stats.html',
        res=res,
        img=img,
    )


@app.route('/del-quiz/<int:quiz_id>')
def del_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8081)
