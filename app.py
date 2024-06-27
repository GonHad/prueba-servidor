from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(100), nullable=False)
    tarjeta_credito = db.Column(db.String(100), nullable=False)
    fecha_expiracion = db.Column(db.String(100), nullable=False)
    codigo_seguridad = db.Column(db.String(100), nullable=False)

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

        new_payment = Payment(
            nombre=nombre, email=email, fecha_nacimiento=fecha_nacimiento,
            dni=dni, tarjeta_credito=tarjeta_credito, fecha_expiracion=fecha_expiracion,
            codigo_seguridad=codigo_seguridad
        )
        db.session.add(new_payment)
        db.session.commit()

        return redirect(url_for('success', email=email))
    return render_template('payment.html')

@app.route('/success')
def success():
    email = request.args.get('email')
    return render_template('success.html', email=email)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
