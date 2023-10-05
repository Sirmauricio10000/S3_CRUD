from pymongo import MongoClient

client = MongoClient('mongodb://18.209.35.24:80/')
db = client['bucket_database']  
lista_archivos = db['lista_archivos']



def crear_elemento(nombre):
    elemento_existente = consultar_elemento_por_nombre(nombre)
    if elemento_existente[0] == False:
        nuevo_elemento = {
            "nombre": nombre
        }

        try:
            lista_archivos.insert_one(nuevo_elemento)
            print(f"Elemento creado: nombre='{nombre}'")
            return {"message": f"Elemento '{nombre}' creado correctamente."}, 201  
        except Exception as e:
            print(f"Error al crear elemento: {str(e)}")
            return {"error": str(e)}, 500 
    else:
        return {"message": f"El elemento '{nombre}' ya existe."}, 400  



def consultar_elementos():
    try:
        elementos = lista_archivos.find({})
        nombres = [elemento["nombre"] for elemento in elementos]
        return nombres, 200
    except Exception as e:
        print(f"Error al consultar elementos: {str(e)}")
        return []



def consultar_elemento_por_nombre(nombre):
    try:
        elemento = lista_archivos.find_one({"nombre": nombre})
        if elemento is None:
            return False, 404
        return True, 200
    except Exception as e:
        print(f"Error al consultar elemento por nombre: {str(e)}")
        return None
    

def eliminar_elemento_por_nombre(nombre):
    try:
        resultado = lista_archivos.delete_one({"nombre": nombre})
        if resultado.deleted_count == 1:
            return {"message": f"Elemento '{nombre}' eliminado correctamente."}, 200
        else:
            return {"message": f"Elemento '{nombre}' no encontrado."}, 404
    except Exception as e:
        return {"error": str(e)}, 500 

