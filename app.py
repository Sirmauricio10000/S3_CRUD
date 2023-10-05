from flask import Flask, redirect, url_for, jsonify
from flask_restx import Api, Resource
from flask_cors import CORS

from connection import crear_elemento, consultar_elementos, consultar_elemento_por_nombre, eliminar_elemento_por_nombre, descargar_elemento

app = Flask(__name__)
CORS(app)

api = Api(
    app,
    doc="/",
    version="0.1",
    title="S3 API",
)


@api.route("/api/swagger", doc = False)
class Swagger(Resource):
    def get(self):
        swagger_url = url_for("api.swagger_json")
        return redirect(swagger_url)
    

@api.route("/lista_elementos")
class ConsultarTodos(Resource):
    def get(self):
        try:
            response = consultar_elementos()
            return response
        except Exception as e:
            return {"error": str(e)}, 500 
        

@api.route("/consultar_elemento/<string:nombre>")
class EliminarElemento(Resource):
    def get(self, nombre):
        try:
            return consultar_elemento_por_nombre(nombre)
        except Exception as e:
            return {"error": str(e)}, 500 
        
        
@api.route("/descargar_elemento/<string:nombre>")
class DescargarElemento(Resource):
    def get(self, nombre):
        try:
            return descargar_elemento(nombre)
        except Exception as e:
            return {"error": str(e)}, 500 

    
@api.route("/crear_elemento/<path:ruta>")
class Crear(Resource):
    def post(self, ruta):
        try:
            return crear_elemento(ruta)
        except Exception as e:
            return {"error": str(e)}, 500
        

@api.route("/eliminar_elemento/<string:nombre>")
class EliminarElemento(Resource):
    def delete(self, nombre):
        try:
            return eliminar_elemento_por_nombre(nombre)
        except Exception as e:
            return {"error": str(e)}, 500 


    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)