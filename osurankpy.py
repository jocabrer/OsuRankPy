import msvcrt
import pycurl
import json
from io import BytesIO 


#Funcion que obtiene una url 
def obtenerUrl(url):
    
    #Buffer de lectura para recibir los datos del cUrl
    b_obj = BytesIO() 
    
    #Libreria cUrl seteamos la url a buscar
    crl = pycurl.Curl() 
    crl.setopt(crl.URL, url)
    
    # Write bytes that are utf-8 encoded
    crl.setopt(crl.WRITEDATA, b_obj)
    
    # Ejecutar la lectura remota y cerramos la sesión
    crl.perform() 
    crl.close()

    # Get the content stored in the BytesIO object (in byte characters) 
    get_body = b_obj.getvalue()
    get_body = get_body.decode('utf8')

    #din de la funcion y retornamos la data extraida de la url
    return get_body


#solicitar nombre de usuario y almacenar el valor.   
print("Ingresar un nombre de jugador OSU")
nombre = input()

#Mostrar mensaje de confirmación 
print(f"Obteniendo datos del usuario, {nombre}... favor espere")

#obtener la url del perfil del jugador
data = obtenerUrl('http://osu.ppy.sh/users/'+nombre)

#dividir la data por líneas
htmlSplit =data.split('\n')

#recorrer las líneas hasta hallar el patrón que me indica la línea de la data que busco 
for linea in range(len(htmlSplit)):
    indice = htmlSplit[linea].find('https://osu.ppy.sh/users/')
    if  indice != -1:
            break

#La pagína de Osu al buscar por nombre de usuario el sisitem automaticamente busca el id que es finalmente el destino 
#Por lo que extraigo esta url final con id para extraer la data.            
direcciones = htmlSplit[linea].split('=')
direccion = direcciones[3]
urlfinal = direccion[6:len(direccion)-5]
urlfinal = 'http'+urlfinal
htmlSplit = obtenerUrl(urlfinal)
htmlSplit = htmlSplit.split('\n')

#ya tengo la data final en HtmlSplit entonces busco el json con los datos.
for linea in range(len(htmlSplit)):
    indice = htmlSplit[linea].find('<script id="json-user" type="application/json">')
    if indice != -1:
        break

#proceso la información del JSON y muestro en pantalla
parsed_json = (json.loads(htmlSplit[linea+1]))
stats = parsed_json['statistics']
print('Hola '+ parsed_json['username'])
stats = parsed_json['statistics']
print('Tu rank actual es ' + str(stats['pp_rank']))

#cerrar el programa.
msvcrt.getch()
