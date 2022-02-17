from flask import Flask, render_template, url_for, request, redirect, flash, session
from dbcon import PostgresManagement


app = Flask(__name__)
app.secret_key = 'grimmteshco'
postgres = PostgresManagement()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        '''
        function to get the users from the db and check the pswd while removing the 
        hash return redirect the index
        '''