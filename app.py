from flask import Flask, render_template ,request, redirect, url_for, flash, session
import psycopg2
app = Flask(__name__)
app.secret_key = '1010'  # Cambia esto por una clave segura

DB_HOST = 'compras.chq68sei2xuw.us-east-1.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'ilich'
DB_PASS = '40910626'


def verificar_usuario(username, password):
    # Conecta a PostgreSQL y verifica si el usuario existe
    conexion = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s", (username, password))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    return usuario

def obtener_datos():
    # Conecta a PostgreSQL y recupera datos de la tabla
    conexion = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM compras")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos

@app.route('/')

def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if verificar_usuario(username, password):
            session['username'] = username  # Guarda el usuario en la sesión
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/index')
def index():
    # Obtiene los datos de la tabla

    #datos = obtener_datos()
    #return render_template('index.html', datos=datos)
    if 'username' in session:
        datos = obtener_datos()
        return render_template('index.html', datos=datos)
    else:
        flash('Debes iniciar sesión primero')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)