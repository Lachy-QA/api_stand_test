# Importe del archivo configuration
import configuration

# Importe del paquete requests
import requests

# Envío de una solicitud mediante la librería requests
# LLamado de la función get(), proporcionándole la URL
# También se pueden incluir encabezados y parámetros si fuese necesario
def get_docs ():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)

response = get_docs()
print(response.status_code)

# # Detalles de la solicitud:
# import configuration: esta línea importa el archivo configuration.py. Esto significa que ahora puedes acceder a las constantes definidas en configuration.py: URL_SERVICE y DOC_PATH.
# import requests: importa la librería Requests.
# def get_docs(): define una función llamada get_docs. Cuando se llama a esta función, realiza una solicitud GET a la combinación de URL_SERVICE y DOC_PATH (es decir, la URL completa de la documentación).
# response = get_docs(): esta línea llama a la función get_docs() y almacena la respuesta en la variable de respuesta.
# print(response.status_code): muestra el código de estado de la respuesta HTTP. Por ejemplo, si todo va bien, debe mostrarse 200, que es el código de estado de "OK".

# Importe del archivo data
import data

# Envío de la solicitud POST
def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # inserta la dirección URL completa
                         json=body,  # inserta el cuerpo de solicitud
                         headers=data.headers)  # inserta los encabezados

response = post_new_user(data.user_body)
print(response.status_code)
# Acá se convierte el cuerpo de la respuesta a un diccionario
response_budy_to_dicc = response.json()
# Acá se imprime el contenido del cuerpo de la respuesta
print(response_budy_to_dicc) 

def get_users_table():
    url = configuration.URL_SERVICE
    response = requests.get(url)
    return response

