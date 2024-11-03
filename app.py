from flask import Flask, render_template
import psycopg2
app = Flask(__name__)

DB_HOST = 'compras.chq68sei2xuw.us-east-1.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'ilich'
DB_PASS = '40910626'



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
def index():
    # Obtiene los datos de la tabla
    datos = obtener_datos()
    return render_template('index.html', datos=datos)


#def home():
#    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)