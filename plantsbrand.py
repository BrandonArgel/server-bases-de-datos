from flask import Flask, render_template, request, url_for, redirect, flash
from flask.globals import session
from flask.helpers import flash
from flask_mysqldb import MySQL, MySQLdb
from flask_bcrypt import bcrypt
brandplantsApp = Flask(__name__)
brandplantsApp.config['MYSQL_HOST'] = 'localhost'
brandplantsApp.config['MYSQL_USER'] = 'root'
brandplantsApp.config['MYSQL_PASSWORD'] = 'mysql'
brandplantsApp.config['MYSQL_DB'] = 'plantsbrand'
brandplantsApp.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(brandplantsApp)
@brandplantsApp.route('/')
def index():
    return render_template('inicio.html')
    
@brandplantsApp.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        correoc = request.form['correo']
        clavec = request.form['clave'].encode('utf-8')
        selcliente = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        selcliente.execute("SELECT * FROM cliente WHERE correoc = %s", (correoc,))
        c = selcliente.fetchone()
        selcliente.close()
        if c is not None:
            if bcrypt.hashpw(clavec, c['clavec'].encode('utf-8')) == c['clavec'].encode('utf-8'):
                session['nombrec'] = c['nombrec']
                session['correoc'] = c['correoc']
                return render_template('cliente.html')
            else:
                flash('Contraseña incorrecta')
                return redirect(request.url)
        else:
            flash('Usuario inexistente')
            return redirect(request.url)
    else:       
        return render_template('login.html')

@brandplantsApp.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@brandplantsApp.route('/cliente', methods = ['GET', 'POST'])
def cliente():
    return render_template('cliente.html')




@brandplantsApp.route('/registro', methods = ['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombrec = request.form['nombrec']
        correoc = request.form['correoc']
        clavec = request.form['clavec'].encode('utf-8')
        clavecifrada = bcrypt.hashpw(clavec, bcrypt.gensalt())
        regcliente = mysql.connection.cursor()
        regcliente.execute("INSERT INTO cliente (nombrec, correoc, clavec) VALUES (%s, %s, %s)", (nombrec, correoc, clavecifrada))
        mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    brandplantsApp.secret_key = 'aaaaeeee'
    brandplantsApp.run(port = 3000,debug = True)

