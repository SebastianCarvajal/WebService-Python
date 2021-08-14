from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


app = Flask(__name__)


#acceso publico
CORS(app)
#cors = CORS(app, resources={r"/contacto/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
    

#conectar con la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost:3306/web_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#instanciar las librerias
db = SQLAlchemy(app)
ma = Marshmallow(app)

#crear la clase para la tabla contactos de la base de datos
class Contactos(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(50))

    def __init__(self, nombre, telefono, email):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

# Esquema para la tabla contacto de la base de datos
class ContactoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'telefono', 'email')

#iniciarlizar esquema >> Una sola respuesta
contacto_Schema = ContactoSchema()
#iniciarlizar esquema >> Varias respuesta
contactos_Schema = ContactoSchema(many=True)


#GET
@app.route('/contacto', methods = ['GET'])
def get_contactos():
    all_contactos = Contactos.query.all()
    result = contactos_Schema.dump(all_contactos)
    return jsonify(result)

#GET Con ID
@app.route('/contacto/<id>', methods = ['GET'])
def get_contactos_id(id):
    un_contacto = Contactos.query.get(id)
    return contacto_Schema.jsonify(un_contacto)

#POST
@app.route('/contacto', methods = ['POST'])
def insert_contacto():
    data = request.get_json()
    nombre = data['nombre']
    telefono = data['telefono']
    email = data['email']

    nuevo_registro = Contactos(nombre, telefono, email)

    db.session.add(nuevo_registro)
    db.session.commit()
    return contacto_Schema.jsonify(nuevo_registro)

#POST2
@app.route('/contacto2', methods = ['POST'])
def insert_contacto2():
    #data = request.get_json()
    nombre = request.args['nombre']
    telefono = request.args['telefono']
    email = request.args['email']

    nuevo_registro = Contactos(nombre, telefono, email)

    db.session.add(nuevo_registro)
    db.session.commit()
    return contacto_Schema.jsonify(nuevo_registro)


# PUT    Modificar
@app.route('/contacto/<id>', methods = ['PUT'])
def update_contacto(id):
    data = request.get_json()
    get_contact = Contactos.query.get(id)
    if data.get('nombre'):
        get_contact.nombre = data['nombre']
    if data.get('telefono'):
        get_contact.telefono = data['telefono']
    if data.get('email'):
        get_contact.email = data['email']
    
    db.session.add(get_contact)
    db.session.commit()
    return contacto_Schema.jsonify(get_contact)

# DELETE eliminar
@app.route('/contacto/<id>', methods = ['DELETE'])
def delete_contacto(id):
    get_contact = Contactos.query.get(id)
    db.session.delete(get_contact)
    db.session.commit()
    return jsonify({"Mensaje":"Se elimino un Contacto"})

#...
@app.route('/', methods = ['GET'])
def index():
    return  jsonify({"Mensaje":"Bienvenido a API"})



if __name__ == "__main__":
    app.run(debug=True)
