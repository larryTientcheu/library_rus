from lib2to3.pgen2.pgen import generate_grammar
import re
from unicodedata import name
from flask.globals import request
from sqlalchemy import true
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


    def editUser(self, request, user):
        uid = user.uid[0]
        username = user.username[0]
        opassword = request.form['old_password']
        
        if func.checkPassword(user.password[0], opassword):
            npassword = request.form['new_password']
            npassword = func.hashPassword(npassword)
            if 'admin' in request.form:
                admin = request.form['admin']
            else:
                admin = False
            user = uid, username, npassword, admin

            if(postgres.editUser(user)):
                return True
            else:
                return False
        else:
            
            return False


    def addBook(self, request):
        name = request.form['name']
        price = request.form['price']
        genre = request.form['genre']
        author = request.form['author']

        book = name, price, genre, author
        postgres.addBook(book)


    def deleteUser(self, uid):
        if (postgres.deleteUser(uid)):
            return True
        else:
            return False


    def editBook(self, request, book):
        bid = book.bid[0]
        name = request.form['name']
        price = request.form['price']
        genre = request.form['genre']
        author = request.form['author']
        
        book = bid, name, price, genre, author
        if(postgres.editBook(book)):
            return True
        else:
            return False     

    def deleteBook(self, bid):
        if (postgres.deleteBook(bid)):
            return True
        else:
            return False

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


    def searched(self, request):
        search = request.form['searched']
        table = request.form['searchTable']
        print (table)
        if table == 'books':
            books = postgres.searchBookName(table, search)
            return books
        if table == 'users':
            users = postgres.searchUserName(table, search)
            return users