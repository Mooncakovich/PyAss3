'''
address = '4Jb9EzcUd6k1gC7GSH2iu6H7UcL2ez3NgvAF8n6a1QDs'
'''
import requests
from flask import Flask, render_template
import psycopg2
from flask import request


conn = psycopg2.connect("dbname=PY user=postgres password=2309")
cur = conn.cursor()


app = Flask(__name__)



@app.route("/main")

def main():

    return render_template('1.html')

@app.route("/result", methods = ['POST', "GET"])
def result():
    
    output = request.form.to_dict()
    adress = output["adress"]

    url = 'https://solana-gateway.moralis.io/nft/mainnet/' + adress + '/metadata'

    headers = {

    "accept": "application/json",
    "X-API-Key": "SWnpmagdLrYt67aFhsaBRRzoubD59cdQkydkZLeljvVREBpWGmpLktfRLZXcvudp"

    }

    response = requests.get(url, headers=headers)
    cur.execute("""SELECT * from data WHERE adress = %s""", (adress,))
    ans = cur.fetchall()  
    if ans!=[]:
        for row in ans:
            print('adress - ', row[0])
            print('data - ', row[1])
            print('fromDB')
        return render_template('2.html', adress = response.text)
    else:
        cur.execute("""INSERT INTO data (adress, data) VALUES (%s, %s);""", (adress, response.text))
        conn.commit()
        print('added to db')
        return render_template('2.html', adress = response.text)
        

if __name__ == '__main__':

    app.run(debug=True)