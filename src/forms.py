from lib2to3.pgen2.pgen import generate_grammar
from unicodedata import name
from flask.globals import request
from dbcon import PostgresManagement
from src.functions import Functions

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

        print(bid)

        rental = bid, uid, issue_date,period
        postgres.addRental(rental)


