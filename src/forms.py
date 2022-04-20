from lib2to3.pgen2.pgen import generate_grammar
import re
from unicodedata import name
from flask.globals import request
from dbcon import PostgresManagement
from src.functions import Functions
from datetime import datetime
from dateutil import parser

postgres = PostgresManagement()
func = Functions()
class VariousForms():
    def __init__(self) -> None:
        pass

    def addUser(self, request):
        username = request.form['username']
        password = request.form['password']
        password = func.hashPassword(password)
        if 'admin' in request.form:
            admin = request.form['admin']
        else:
            admin = False
        user = username, password, admin
        postgres.addUser(user)


    def editUser(self, request):
        uid = request.form['uid']
        username = request.form['username']
        password = request.form['password']
        password = func.hashPassword(password)
        if 'admin' in request.form:
            admin = request.form['admin']
        else:
            admin = False
        user = uid, username, password, admin
        #postgres.editUser(user) finish this function in dbcon


    def addBook(self, request):
        name = request.form['name']
        price = request.form['price']
        genre = request.form['genre']
        author = request.form['author']

        book = name, price, genre, author
        postgres.addBook(book)

    def addRental(self, request):
        bid = request.form['bid']
        uid = request.form['uid']
        issue_date = request.form['issue_date']
        period = request.form['period']

        rental = bid, uid, issue_date,period
        postgres.addRental(rental)

    def returnRental(self, request):
        rid = int(request.form['rid'])
        issueDate = postgres.findRental(rid)['issuedate'][0]
        
        returnDate = request.form['return_date']
        rDate = parser.parse(returnDate).date()
        fine = func.calculateFine(rDate, issueDate).days

        rental = returnDate, fine, rid
        print(rental[0])
        postgres.returnRental(rental)


