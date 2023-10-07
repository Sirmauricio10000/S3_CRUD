import os
from pymongo import MongoClient
from bucket import upload_to_bucket, delete_from_bucket, download_from_bucket


client = MongoClient('mongodb://54.166.171.58:80/')
db = client['bucket_database']  
lista_archivos = db['lista_archivos']



def subir_elemento(ruta):
    test = test_connection()
    if test != True: return test

    if os.path.exists(ruta):
        nombre = os.path.basename(ruta) 

        
        elemento_existente = consultar_elemento_por_nombre(nombre)
        if elemento_existente[0] == False:
            nuevo_elemento = {
                "nombre": nombre
            }

            try:
                subir = upload_to_bucket(ruta, nombre)
                if subir != True:
                    return {"error_bucket": subir}, 500 

                lista_archivos.insert_one(nuevo_elemento)
                print(f"Elemento creado: nombre='{nombre}'")
                
                return {"message": f"Elemento '{nombre}' subido correctamente."}, 201  
            except Exception as e:
                print(f"Error al crear elemento: {str(e)}")
                return {"error": str(e)}, 500 
        else:
            return {"message": f"El elemento '{nombre}' ya existe."}, 400
    else:
        return {"error": "El archivo no existe en la ruta especificada."}, 404



def consultar_elementos():
    test = test_connection()
    if test != True: return test

    try:
        elementos = lista_archivos.find({})
        nombres = [elemento["nombre"] for elemento in elementos]
        return nombres, 200
    except Exception as e:
        print(f"Error al consultar elementos: {str(e)}")
        return []



def consultar_elemento_por_nombre(nombre):

    test = test_connection()
    if test != True: return test

    try:
        elemento = lista_archivos.find_one({"nombre": nombre})
        if elemento is None:
            return False, 404
        return True, 200
    except Exception as e:
        print(f"Error al consultar elemento por nombre: {str(e)}")
        return None
    

def eliminar_elemento_por_nombre(nombre):

    test = test_connection()
    if test != True: return test

    try:
        eliminar = delete_from_bucket(nombre)
        if eliminar != True:
            return {"error_bucket": eliminar}, 500 
        
        resultado = lista_archivos.delete_one({"nombre": nombre})
        if resultado.deleted_count == 1:
            return {"message": f"Elemento '{nombre}' eliminado correctamente."}, 200
        else:
            return {"message": f"Elemento '{nombre}' no encontrado."}, 404
    except Exception as e:
        return {"error": str(e)}, 500 
    

def descargar_elemento(nombre):

    test = test_connection()
    if test != True: return test

    elemento_existente = consultar_elemento_por_nombre(nombre)
    if elemento_existente[0] == False:
        return {"message": f"Elemento '{nombre}' no encontrado en la base de datos."}, 404
    else:
        try:
            resultado = download_from_bucket(nombre)
            return resultado
        except Exception as e:
            return {"error": str(e)}, 500 
        
def test_connection():
    try:
        db.command("ping")
        return True

    except Exception as e:
        return {"error": "cannot connect to database. " + str(e)}, 500 



        

