#Practica Python, Flask con Flask-SQLAlchemy y MySQL
#Alumno: José Torres
#Arquitectura Orientada a Microservicios

#Importamos los modulos o librerias a usar
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Construimos la applicación
app=Flask(__name__)

#Creamos la conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:<contraseña>@localhost:<puerto>/<nombre_bd>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
ma=Marshmallow(app)

#Creamos una clase (Tareas). 
#Definicmos y modelamos las tablas en la base de datos
class Tarea(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(60),unique=True)
    descripcion=db.Column(db.String(250))
    
    def __init__(self, nombre, descripcion):
        self.nombre= nombre
        self.descripcion=descripcion

#Con este comando creamos las tablas
with app.app_context():
    db.create_all()

#Creanos una clase (TareaEsquema)
#Un esquema organiza los datos dentro de una base de datos relacional

class TareaEsquema(ma.Schema):
    class Meta:
        fields=('id', 'nombre', 'descripcion')

#Crear una sola tarea
tarea_esquema=TareaEsquema()

#Crear varias tareas
tareas_esquema=TareaEsquema(many=True)

#Creamos las rutas de la aplicación
#Crear una tarea con POST
@app.route('/tareas',methods=['POST'])
def crear_tarea():
    nombre=request.json['nombre']
    descripcion=request.json['descripcion']

    nueva_tarea=Tarea(nombre, descripcion)

    #Guarda en la base de datos
    db.session.add(nueva_tarea)
    db.session.commit()

    return tarea_esquema.jsonify(nueva_tarea)
    
    #print(request.json)
    #return 'Recibido'

#Obtener todas las tareas con GET
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
    todas_las_tareas=Tarea.query.all()
    result=tareas_esquema.dump(todas_las_tareas)
    return jsonify(result)

#Obtener una sola tarea
@app.route('/tareas/<id>',methods=['GET'])
def obtener_tarea(id):
    tarea=Tarea.query.get(id)
    return tarea_esquema.jsonify(tarea)

#Actualizar los datos con PUT
@app.route('/tareas/<id>',methods=['PUT'])
def actualizar_Tarea(id):
    tarea=Tarea.query.get(id)

    nombre=request.json['nombre']
    descripcion=request.json['descripcion']

    tarea.nombre=nombre
    tarea.descripcion=descripcion

    db.session.commit()
    return tarea_esquema.jsonify(tarea)

#Borrar una tarea con DELETE
@app.route('/tareas/<id>', methods=['DELETE'])
def borrar_tarea(id):
    tarea=Tarea.query.get(id)
    db.session.delete(tarea)
    db.session.commit()

    return tarea_esquema.jsonify(tarea)

#Creando una ruta principal (index) con mensaje
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Bienevendi@ a mi API REST MySQl x SQLAlquemy, para la clase de Arquitectura Orientado a Microservicios'})

if __name__=="__main__":
    app.run(debug=True)