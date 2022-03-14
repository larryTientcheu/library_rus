from datetime import timedelta
from flask import Flask, render_template, url_for, request, redirect, flash, session
from dbcon import PostgresManagement
from src.functions import Functions
from src.forms import VariousForms

postgres =PostgresManagement()
func = Functions()
forms = VariousForms()

app = Flask(__name__)
app.secret_key = 'grimmteshco'

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged' not in session:
        #session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        if request.method == 'POST':
            '''
            function to get the users from the db and check the pswd while removing the 
            hash return redirect the index
            '''
            if request.form['username'] and request.form['password']:
                user = postgres.findUser(request.form['username'])
                if len(user) > 0 and func.checkPassword(user.password[0], request.form['password']):
                    #flash('You were successfully logged in')
                    session['logged'] = True
                    session['username'] = user.username[0]
                    return redirect(url_for('index'))
                else:
                    error = 'Invalid Username or Password'
                    session.pop('logged', None)
            else:
                error = 'Please enter Username and Password'
                session.pop('logged', None)
        return render_template('pages/login.html', error=error)
    else:
        return render_template('index.html')

    

@app.route('/index')
def index():
    if 'logged' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/users')
def users():
    if 'logged' in session:
        users = postgres.findUsers()
        return render_template('pages/users.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if 'logged' in session:
        if request.method == 'POST' and len(request.form) > 0:
            forms.addNewUser(request)
            return redirect(url_for('users'))
        return render_template('forms/new_user.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)