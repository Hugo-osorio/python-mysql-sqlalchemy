from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Se instancia Flask en un objeto llamado app
app = Flask(__name__)

# Se configura la base de datos a la que va a acceder con el usuario, contraseña y URI de la base de datos
app.config['SQL_ALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost:8080/flaskmysql'
# Se configura la variable del diccionario config en el objeto app con un boleano False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Se crea un objeto desde SQLAlchemy
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    # Con esta linea defino una nueva columna con ayuda del metodo db.Column
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100),)
    # El ORM(Object Relational Mapper) crea las base de datos por nosotros con ayuda de esta sintaxis
    # ORM -> constructor de bases de datos de alto nivel

    def __init__(self, title, description):
        # Este inicializador va a inicializar mis variables
        self.title = title
        self.description = description

db.create_all() # We create the initial database

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():
    
    title = request.json['title']
    description = request.json['description']

    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=4000)