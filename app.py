from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///site.db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class TaskInMemory:
    tasks = []
    id_counter = 1

    def __init__(self, content, user_id):
        self.id = TaskInMemory.id_counter
        TaskInMemory.id_counter += 1
        self.content = content
        self.done = False
        self.user_id = user_id
        TaskInMemory.tasks.append(self)

    @classmethod
    def get_user_tasks(cls, user_id):
        return [task for task in cls.tasks if task.user_id == user_id]

    @classmethod
    def get_task_by_id(cls, task_id):
        return next((task for task in cls.tasks if task.id == task_id), None)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

def is_valid_username(username):
    return username and 4 <= len(username) <= 20

def is_valid_password(password):
    return password and len(password) >= 6

@app.route('/add')
def index():
    if 'user_id' not in session:
        flash('Você precisa estar logado para visualizar suas tarefas.', 'danger')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_tasks = TaskInMemory.get_user_tasks(user_id)
    return render_template('index.html', tasks=user_tasks)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('Você precisa estar logado para adicionar tarefas.', 'danger')
        return redirect(url_for('login'))

    content = request.form['content']
    user_id = session['user_id']
    new_task = TaskInMemory(content=content, user_id=user_id)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'create_account' in request.form:
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')

            if not is_valid_username(new_username) or not is_valid_password(new_password):
                flash('Por favor, forneça um nome de usuário e senha válidos.', 'danger')
                return redirect(url_for('login'))

            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash('Nome de usuário já existe. Escolha outro.', 'danger')
            else:
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                new_user = User(username=new_username, password=hashed_password)

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Conta criada com sucesso! Faça o login agora.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Erro ao criar conta: {str(e)}', 'danger')

        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, forneça um nome de usuário e senha válidos.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login falhou. Verifique seu nome de usuário e senha.', 'danger')

    return render_template('login.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TaskInMemory.get_task_by_id(id)
    if task_to_delete:
        TaskInMemory.tasks.remove(task_to_delete)
    return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('user_id', None)
        flash('Logout bem-sucedido!', 'success')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
