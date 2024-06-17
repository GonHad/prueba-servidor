from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from config import config
import os

app = Flask(__name__)

def get_db_connection():
    params = config()
    try:
        conn = psycopg2.connect(params['database_url'])
        return conn
    except psycopg2.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        dni = request.form['dni']
        tarjeta_credito = request.form['tarjeta_credito']
        fecha_expiracion = request.form['fecha_expiracion']
        codigo_seguridad = request.form['codigo_seguridad']

        conn = get_db_connection()
        if conn is None:
            return "Internal Server Error: Database connection failed", 500
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO compradores (nombre, email, fecha_nacimiento, dni, tarjeta_credito, fecha_expiracion, codigo_seguridad) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nombre, email, fecha_nacimiento, dni, tarjeta_credito, fecha_expiracion, codigo_seguridad)
        )
        conn.commit()
        cur.close()
        conn.close()

        # Redirigir a la página de éxito con el correo electrónico del comprador
        return redirect(url_for('success', email=email))
    return render_template('payment.html')

@app.route('/success')
def success():
    email = request.args.get('email')
    return render_template('success.html', email=email)

if __name__ == '__main__':
    from os import environ
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)))
