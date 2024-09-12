from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Task
from . import db
from .forms import TaskForm

main = Blueprint('main', __name__)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já registrado. Faça login.', 'danger')
            return redirect(url_for('main.login'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email ou senha incorretos. Tente novamente.', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    user_tasks = Task.query.filter(
        (Task.user_id == current_user.id) |
        (Task.shared_with.any(id=current_user.id))
    ).all()

    other_users_tasks = Task.query.filter(
        (Task.user_id != current_user.id) &
        ~Task.shared_with.any(id=current_user.id)
    ).all()

    tasks_shared_with_others = [task for task in other_users_tasks if task.shared_with]
    tasks_not_shared = [task for task in other_users_tasks if not task.shared_with]

    return render_template(
        'dashboard.html',
        user_tasks=user_tasks,
        tasks_shared_with_others=tasks_shared_with_others,
        tasks_not_shared=tasks_not_shared
    )

@main.route('/task/new', methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    form.shared_with.choices = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all()]

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        status = form.status.data
        shared_with_ids = request.form.getlist('shared_with')

        new_task = Task(
            title=title,
            description=description,
            status=status,
            owner=current_user
        )

        if shared_with_ids:
            users_to_share = User.query.filter(User.id.in_(shared_with_ids)).all()
            new_task.shared_with.extend(users_to_share)

        db.session.add(new_task)
        db.session.commit()
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('task_form.html', form=form, task=None)



@main.route('/task/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)

    if current_user != task.owner and current_user not in task.shared_with:
        flash('Você não tem permissão para editar esta tarefa.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = TaskForm(obj=task)

    if current_user == task.owner:
        form.shared_with.choices = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all()]
        form.shared_with.data = [user.id for user in task.shared_with]
    else:
        del form.shared_with

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data

        if current_user == task.owner:
            shared_user_ids = request.form.getlist('shared_with')
            task.shared_with = User.query.filter(User.id.in_(shared_user_ids)).all()

        try:
            db.session.commit()
            flash('Tarefa atualizada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar a tarefa: {e}', 'danger')

        return redirect(url_for('main.dashboard'))

    return render_template('task_form.html', form=form, task=task)

@main.route('/task/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if current_user != task.owner and current_user not in task.shared_with:
        flash('Você não tem permissão para deletar esta tarefa.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Tarefa deletada com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Usuário deletado com sucesso!', 'success')
        else:
            flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('main.list_users'))

    users = User.query.all()
    return render_template('users.html', users=users)
