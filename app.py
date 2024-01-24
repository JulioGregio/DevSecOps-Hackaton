from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123mudar@localhost:3306/cadastro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Altere isso para uma chave secreta forte
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class TaskInMemory:
    tasks = []
    id_counter = 1

    def __init__(self, content):
        self.id = TaskInMemory.id_counter
        TaskInMemory.id_counter += 1
        self.content = content
        self.done = False
        TaskInMemory.tasks.append(self)

    @classmethod
    def get_task_by_id(cls, task_id):
        return next((task for task in cls.tasks if task.id == task_id), None)

    @classmethod
    def get_all_tasks(cls):
        return cls.tasks

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/add')
def index():
    tasks = TaskInMemory.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    if 'user_id' not in session:
        flash('Você precisa estar logado para adicionar tarefas.', 'danger')
        return redirect(url_for('login'))

    content = request.form['content']
    new_task = TaskInMemory(content=content)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = TaskInMemory.get_task_by_id(id)
    if task_to_delete:
        TaskInMemory.tasks.remove(task_to_delete)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verifica se o usuário está tentando criar uma conta
        if 'create_account' in request.form:
            new_username = request.form.get('new_username')
            new_password = request.form.get('new_password')

            if not new_username or not new_password:
                flash('Por favor, forneça um nome de usuário e senha válidos.', 'danger')
                return redirect(url_for('login'))

            # Verifique se o novo usuário já existe
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user:
                flash('Nome de usuário já existe. Escolha outro.', 'danger')
            else:
                # Cria o novo usuário
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                new_user = User(username=new_username, password=hashed_password)

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Conta criada com sucesso! Faça o login agora.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(f'Erro ao criar conta: {str(e)}', 'danger')

        # Se não estiver criando uma conta, verifica o login normal
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Por favor, forneça um nome de usuário e senha válidos.', 'danger')
            return redirect(url_for('login'))

        # Verifica se o usuário está tentando fazer login
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Armazena o ID do usuário na sessão
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login falhou. Verifique seu nome de usuário e senha.', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
