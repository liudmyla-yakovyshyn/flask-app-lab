from flask import request, render_template
from app import app


@app.route('/')
@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме | Людмила Яковишин')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title='Контакти | Людмила Яковишин')


@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', agent=agent)