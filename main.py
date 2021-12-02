import sqlalchemy as sqlalchemy
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diccionario.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class diccionario(db.Model):
    __tablename__ = 'diccionario'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    palabra = sqlalchemy.Column(sqlalchemy.String(length=100))
    significado = sqlalchemy.Column(sqlalchemy.String(length=300))

def __init__(self, id, palabra, significado):
   self.id = id
   self.palabra = palabra
   self.significado = significado

db.create_all()
@app.route("/")
def base():
    return render_template("base.html")

@app.route("/agregar", methods = ['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        if not request.form['palabra'] or not request.form['significado']:
            flash('Por favor, ingresa todos los datos', 'error')
        else:
            palabra = diccionario(palabra=request.form['palabra'], significado=request.form['significado'])
            db.session.add(palabra)
            db.session.commit()

            return redirect(url_for('base'))
    return render_template("agregar.html")

@app.route("/editar", methods = ['GET', 'POST'])
def editar():
    if request.method == 'POST':
        if not request.form['palabra'] or not request.form['significado']:
            flash('Por favor, ingresa todos los datos', 'error')
        else:
            palabra = db.session.query(diccionario).filter_by(palabra=request.form['palabra']).first()
            db.session.delete(palabra)
            palabran = diccionario(palabra = request.form['palabra'], significado = request.form['significado'])
            db.session.add(palabran)
            db.session.commit()

            return redirect(url_for('base'))
    return render_template("editar.html")


@app.route("/eliminar", methods = ['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        palabra = db.session.query(diccionario).filter_by(palabra=request.form['palabra']).first()
        db.session.delete(palabra)
        db.session.commit()
        return redirect(url_for('base'))
    return render_template("eliminar.html")

@app.route("/lista")
def lista():
    return render_template("lista.html", diccionario = diccionario.query.all())


if __name__ == "__main__":
    app.run(debug=True)