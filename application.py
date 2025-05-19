from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)

# Use SQLite as the databaseihidhishdishidshidhsidhisdhishdiowj9ewjiodhiwhdiwhdwidhishdis
basedir = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database tables
with application.app_context():
    db.create_all()

@application.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@application.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

@application.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

@application.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
