from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, CreateTaskForm
from app.models import User, Task
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
	flash("Bienvenido " + current_user.username + "!")
	tasks = current_user.tasks
	return render_template('index.html', title='Listado', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
	form = CreateTaskForm()
	if form.validate_on_submit():
		task = Task(body=form.body.data, author=current_user, completed=False)
		db.session.add(task)
		db.session.commit()
		flash('Tarea añadida exitosamente!')
		return redirect(url_for('index'))
	return render_template('createTask.html', title='Crear Tarea', form=form)

@app.route('/update')
def update():
    task_id = request.args.get('id')
    task = Task.query.get(task_id)
    if task is None:
    	flash('Tarea inexistente!')
    	return redirect(url_for('index'))
    if task.author.username == current_user.username:
    	if task.completed == False:
    		task.completed = True
    	else:
    		task.completed = False
    	db.session.commit()
    	flash('Tarea actualizada exitosamente!')
    	return redirect(url_for('index'))
    else:
    	flash('No puedes actualizar esta tarea!')
    	return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Usuario o clave inválidos')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Ingreso', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Felicidades, ya eres un usuario registrado!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Registro', form=form)

