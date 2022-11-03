from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from flask import request
import requests



#db connection
def get_db_connection():
    conn = psycopg2.connect("dbname=FlaskProject user=postgres password=2309")
    return conn

class User(object):    
    def __init__(self, loggined, user_login):
        self.loggined = loggined
        self.user_login = user_login
    def UserLoggedIn(self):
        self.loggined = True
    def UserLoggedOut(self):
        self.loggined = False
    def SetUsername(self, username):
        self.user_login = username
    def GetUsername(self):
        return(self.user_login)
    def LoggedIn(self):
        return(self.loggined)

user = User(False, 'username')
#flask apps
app = Flask(__name__)


@app.route("/registration", methods = ['POST', "GET"])
def registration():
    user.UserLoggedOut()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, hashed_password)'
                    'VALUES (%s, %s)',
                    (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('login'), 301)
    return render_template('registration.html')


@app.route("/login", methods = ['POST', "GET"])
def login():
    user.UserLoggedOut()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        rows = cur.fetchall()
        for row in rows:
            if row[0] == username and row[1] == password:
                cur.close()
                conn.close()
                user.UserLoggedIn()
                user.SetUsername(username)
                return redirect(url_for('main'), 301)
        cur.close()
        conn.close()
        return render_template('login.html')
    return render_template('login.html')


@app.route("/main")
def main():
    if user.LoggedIn():
        return render_template('main.html', username = user.GetUsername())
    else:
       return redirect(url_for('login'), 301) 


@app.route("/result", methods = ['POST', "GET"])
def result():
    if user.LoggedIn():
        output = request.form.to_dict()
        adress = output["adress"]

        url = 'https://solana-gateway.moralis.io/nft/mainnet/' + adress + '/metadata'

        headers = {

        "accept": "application/json",
        "X-API-Key": "SWnpmagdLrYt67aFhsaBRRzoubD59cdQkydkZLeljvVREBpWGmpLktfRLZXcvudp"

        }

        response = requests.get(url, headers=headers)
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""SELECT * from data WHERE adress = %s""", (adress,))
        ans = cur.fetchall()  
        if ans!=[]:
            for row in ans:
                print('adress - ', row[0])
                print('data - ', row[1])
                print('fromDB')
            cur.close()
            conn.close()
            return render_template('result.html', adress = response.text, username = user.GetUsername())
        else:
            cur.execute("""INSERT INTO data (adress, data) VALUES (%s, %s);""", (adress, response.text))
            conn.commit()
            cur.close()
            conn.close()
            print('added to db')
            return render_template('result.html', adress = response.text, username = user.GetUsername())
    else:
       return redirect(url_for('login'), 301) 

if __name__ == '__main__':

    app.run(debug=True)