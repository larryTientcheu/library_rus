from flask.globals import request
from dbcon import PostgresManagement
from src.functions import Functions

postgres = PostgresManagement()
func = Functions()
class VariousForms():
    def __init__(self) -> None:
        pass

    def addNewUser(self, request):
        username = request.form['username']
        password = request.form['password']
        password = func.hashPassword(password)
        if 'admin' in request.form:
            admin = request.form['admin']
        else:
            admin = False
        user = username, password, admin
        postgres.addUser(user)


