from winreg import QueryInfoKey, QueryValue
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from sqlalchemy import create_engine
from json import dumps
import mysql.connector
from django.http import HttpResponse
#Precisa instalar os 4 pacotes: clica em packages e digita o nome do pacote
#Flask
#Flask-SQLAlchemy
#Flask-Restful
#Jsonify
# Conectando ao BD exemplo feito em SQLLITE
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="ceci"
)

mycursor = db.cursor()
##Coloca o servidor Web no ar 
app = Flask(__name__)
api = Api(app)
cors = CORS(app)
class UsersLogin(Resource):
    def post(self):
        email = request.json['email']
        senha = request.json["senha"]
        sql = "select * from user where email = %s and senha= %s"
        val = (email, senha)
        mycursor.execute(sql, val)
        print(mycursor.fetchone())
class Users(Resource):
    def get(self):
        mycursor.execute("select * from user")
        print(mycursor.fetchone())
        return mycursor.fetchone()
    def post(self): # Inclui no BD um usuário passado como parâmetro
        nome = request.json['nome']
        email = request.json['email']
        senha = request.json['senha']
        telefone = request.json['telefone']


        sql = "insert into user VALUES ( %s, %s, %s, %s)"
        val = ( nome, email, senha, telefone)
        mycursor.execute(sql, val)

        db.commit()
    def put(self): # Update*(atualizar) no BD de um usuário passado como parâmetro

        nome = request.json['nome']
        email = request.json['email']
        telefone = request.json['telefone']

        mycursor.execute("update user set nome ='" + str(nome) +
                     "', email ='" + str(email) + "', telefone ='" + str(telefone) + "'  where email =%d ")

        query = mycursor.execute("select * from user where id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
class UserById(Resource): # Deleta no BD de um usuário passado como parâmetro
    def delete(self, id):
        mycursor.execute("delete from user where id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):

        query = mycursor.execute("select * from user where id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class Address(Resource):
    def get(self): # Mostra todos os usuários cadastrados no BD
        query = mycursor.execute("select * from address")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self): # Inclui no BD um usuário passado como parâmetro
        user_id = request.json['user_id']
        estado = request.json['estado']
        cidade = request.json['cidade']
        rua = request.json['rua']
        numero = request.json['numero']
        complemento = request.json['complemento']
        mycursor.execute(
            "insert into address values('{0}', '{1}','{2}','{3}','{4}','{5}')".format(user_id,estado, cidade, rua, numero, complemento))

        query = mycursor.execute('select * from address order by user_id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self): # Update*(atualizar) no BD de um usuário passado como parâmetro
        user_id = request.json['user_id']
        estado = request.json['estado']
        cidade = request.json['cidade']
        rua = request.json['rua']
        numero = request.json['numero']
        complemento = request.json['complemento']

        mycursor.execute("update address set estado ='" + str(estado) +"', cidade ='" + str(cidade) + "', rua ='" + str(rua) + "', numero = '" + str(numero) + "', complemento = '"+str(complemento)+"'  where user_id=%s " % user_id)

        query = mycursor.execute("select * from address where id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class AddressById(Resource): # Deleta no BD de um usuário passado como parâmetro
    def delete(self, id):

        mycursor.execute("delete from address where user_id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):
        query = mycursor.execute("select * from address where user_id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
class Consulta(Resource):
    def get(self): # Mostra todos os usuários cadastrados no BD

        query = mycursor.execute("select * from consulta")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self): # Inclui no BD um usuário passado como parâmetro
        user_id = request.json['user_id']
        especialidade = request.json['especialidade']
        data = request.json['data']
        hora = request.json['hora']

        mycursor.execute(
            "insert into consulta values('{0}', '{1}','{2}','{3}')".format(user_id,especialidade, data, hora))

        query = mycursor.execute('select * from consulta order by user_id desc limit 1')
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def put(self): # Update*(atualizar) no BD de um usuário passado como parâmetro
      
        especialidade = request.json['especialidade']
        data = request.json['data']
        hora = request.json['hora']


        mycursor.execute("update consulta set especialidade ='" + str(especialidade) +"', data ='" + str(data) + "', hora ='" + str(hora) + "'  where user_id =%d " % int(id))

        query = mycursor.execute("select * from consulta where user_id=%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class ConsultaById(Resource): # Deleta no BD de um usuário passado como parâmetro
    def delete(self, id):

        mycursor.execute("delete from consulta where user_id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):
        
        query = mycursor.execute("select * from consulta where user_id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)



api.add_resource(Users, '/users') 
api.add_resource(UsersLogin, '/users/login') 
api.add_resource(UserById, '/users/<id>') 
api.add_resource(Address, '/address')
api.add_resource(AddressById, '/address/<id>') 
api.add_resource(Consulta, '/consulta')
api.add_resource(ConsultaById, '/consulta/<id>')


  
if __name__ == '__main__':
    app.run(host='0.0.0.0')