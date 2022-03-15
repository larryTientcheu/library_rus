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
                    session['logged'] = True
                    session['username'] = user.username[0]
                    flash('You were successfully logged in as {}'.format(session['username']))
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
            forms.addUser(request)
            return redirect(url_for('users'))
        return render_template('forms/new_user.html')
    else:
        return redirect(url_for('index'))

@app.route('/books')
def books():
    if 'logged' in session:
        books = postgres.findBooks()
        return render_template('pages/books.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/new_book', methods=['GET','POST'])
def new_book():
    if 'logged' in session:
        if request.method == 'POST' and len(request.form) > 0:
            forms.addBook(request)
            return redirect(url_for('books'))
        return render_template('forms/new_book.html')
    else:
        return redirect(url_for('index'))


@app.route('/issued_books')
def issued_books():
    if 'logged' in session:
        ibooks = postgres.findRentals()
        return render_template('pages/issued_books.html', ibooks=ibooks)
    else:
        return redirect(url_for('login'))
    
if __name__ == '__main__':
    app.run(debug=True)