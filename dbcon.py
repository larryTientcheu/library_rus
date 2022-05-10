
import psycopg2
import credent as creds
import pandas as pd
import os


## ****** LOAD PSQL DATABASE ***** ##
class PostgresManagement:
    def __init__(self):
        # Set up a connection to the postgres server.
        conn_string = "host=" + creds.PGHOST + " port=" + "5432" + " dbname=" + creds.PGDATABASE + " user=" + creds.PGUSER \
            + " password=" + creds.PGPASSWORD
        #conn = psycopg2.connect(conn_string)

        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        self.connection = conn
        self.cursor = conn.cursor()
        self.schema = 'public'

    def findUsers(self):
        sql_command = "SELECT * FROM users;"
        data = pd.read_sql(sql_command, self.connection)
        return data

    def findUser(self, username):
        sql_command = "SELECT * FROM users WHERE username ='{}' LIMIT 1".format(
            username)
        # print(sql_command)
        try:
            data = pd.read_sql(sql_command, self.connection)
            return data
        except:
            return ''

    def findUserById(self, uid):
        sql_command = "SELECT * FROM users WHERE uid = '{}' LIMIT 1".format(uid)
        try:
            data = pd.read_sql(sql_command, self.connection)
            return data
        except:
            return ''

    def findBooks(self):
        sql_command = "SELECT * FROM books;"
        data = pd.read_sql(sql_command, self.connection)
        return data

    def findBook(self, bid):
        sql_command = "SELECT * FROM books WHERE bid='{}'".format(bid)
        try:
            data = pd.read_sql(sql_command, self.connection)
            return data
        except:
            return ''

    def findRentals(self):
        sql_command = "SELECT * FROM rental;"
        data = pd.read_sql(sql_command, self.connection)
        return data

    def findRental(self, rid):
        sql_command = "SELECT * FROM rental WHERE rid='{}'".format(rid)
        try:
            data = pd.read_sql(sql_command, self.connection)
            return data
        except:
            return ''

    def findReturnBooks(self):
        sql_command = "SELECT rid,books.bid,users.uid,issuedate,period,returndate,fine,username,books.name,books.author FROM rental INNER JOIN users ON rental.uid = users.uid INNER JOIN books ON rental.bid = books.bid WHERE rental.returndate is NULL AND rental.fine is NULL"
        try:
            data = pd.read_sql(sql_command, self.connection)
            return data
        except:
            return ''

    ### CRUD SECTION REMEMBER TO REMOVE ALL THE PRINT SECTIONS ####
    ##Create##
    def addUser(self, user):
        sql_command = 'INSERT INTO users (username,password,admin) values {}'.format(
            user)
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('inserted')
        except:
            self.connection.rollback()
            print('error')

    def addBook(self, book):
        sql_command = 'INSERT INTO books (name, price, genre, author) values {}'.format(
            book)
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('inserted')
        except:
            self.connection.rollback()
            print('error')

    def addRental(self, rental):
        sql_command = 'INSERT INTO rental (bid,uid,issuedate,period) values {}'.format(
            rental)
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('inserted')
        except:
            self.connection.rollback()
            print('error')

    def returnRental(self,rental):
        sql_command ="UPDATE rental SET returndate = '{}', fine = '{}' where rid = '{}'".format(rental[0],rental[1],rental[2])
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('inserted')
        except:
            self.connection.rollback()
            print('error')

    ##Update##

    def editUser(self, user):
        sql_command = "UPDATE users SET \"password\" = '{}', \"admin\" = '{}' where uid='{}'".format(user[2],user[3],user[0])
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('updated')
            return True
        except:
            self.connection.rollback()
            print('error')
            return False

    def editBook(self, book):
        sql_command = "UPDATE books SET \"name\" = '{}', price = '{}', genre='{}', author ='{}' where bid='{}'".format(book[1],book[2],book[3],book[4], book[0])
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('updated')
            return True
        except:
            self.connection.rollback()
            print('error')
            return False

    ### DELETE
    def deleteUser(self, uid):
        sql_command = "DELETE FROM users where uid={}".format(uid)
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('deleted')
            return True
        except:
            self.connection.rollback()
            print('error')
            return False

    def deleteBook(self, bid):
        sql_command = "DELETE FROM books where bid={}".format(bid)
        print(sql_command)
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            print('deleted')
            return True
        except:
            self.connection.rollback()
            print('error')
            return False
            

    # Search functions
    def searchBookName(self, table, name):
        sql_command = "SELECT * FROM {} where LOWER(\"name\") like'%{}%' ORDER BY name DESC".format(table, name)
        print(sql_command)
        data = pd.read_sql(sql_command, self.connection)
        return data

    def searchUserName(self, table, name):
        sql_command = "SELECT * FROM {} where LOWER(\"username\") like'%{}%' ORDER BY username DESC".format(table, name)
        print(sql_command)
        data = pd.read_sql(sql_command, self.connection)
        return data


if __name__ == "__main__":
    postgresDB = PostgresManagement()
    #print(postgresDB.findUsers())
