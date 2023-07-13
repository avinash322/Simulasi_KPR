from flask import Flask
from flask import render_template
from flask import Flask
from flask import request
from flask_mysqldb import MySQL



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'databaseKPR'

mysql = MySQL(app)

@app.route("/", methods=["GET", "POST"])
def index():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT namarumah,hargarumah FROM rumah''')
    data = cur.fetchall() 
    if request.method == "POST":
        hargarumah = request.form["hargarumah"]
        sukubunga = request.form['rangebunga']
        waktupinjaman = request.form['rangewaktu']
        cur.execute('''SELECT namarumah FROM rumah WHERE hargarumah =%s''', [hargarumah])
        data = cur.fetchall() 
        nilaibungapinjamanawal  = (((int(hargarumah) * int(sukubunga))/100) * int(waktupinjaman))/(int(waktupinjaman)*12)
        nilaipokokpinjamanperbulan = int(hargarumah)// (int(waktupinjaman)*12)
        pinjamanperbulan = int(nilaibungapinjamanawal) + int(nilaipokokpinjamanperbulan)
        totalpinjaman = int(pinjamanperbulan) * (int(waktupinjaman)*12)
        totalbunga = int(totalpinjaman) - int(hargarumah)
        return render_template('output.html',data = data , hargarumah = hargarumah,sukubunga = sukubunga,waktupinjaman = waktupinjaman,nilaibungapinjamanawal = nilaibungapinjamanawal,
        nilaipokokpinjamanperbulan = nilaipokokpinjamanperbulan,pinjamanperbulan = pinjamanperbulan,totalpinjaman = totalpinjaman,totalbunga = totalbunga)
        
    return render_template('index.html',data = data)


@app.route('/output')
def output():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT namarumah,hargarumah FROM rumah''')
    data = cur.fetchall() 
    return render_template('index.html',data = data)




if __name__ == "__main__":
    app.debug = True
    app.run()