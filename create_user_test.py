# Importar los paquetes sender_stand_request y data
import sender_stand_request
import data
from data import user_body


# Escribir la función get_user_body(name)
def get_user_body(first_name):
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    # Copiar el cuerpo de la solicitud desde data.py
    current_body = data.user_body.copy()
    # Cambiar el valor del parámetro firstName con el nombre que pasamos como argumento
    current_body["firstName"] = first_name
    # Devolver un nuevo diccionario con el valor firstName requerido
    return current_body

# Prueba 1. Creación de un nuevo usuario
# El parámetro "firstName" contiene dos caracteres
# Crear una función llamada: test_create_user_2_letter_in_first_name_get_success_response()
def test_create_user_2_letter_in_first_name_get_success_response():
    # Guardar el cuerpo de la solicitud llamado Aa en la varible user_body
    # La versión actualizada del cuerpo de solicitud con el nombre "Aa" se guarda en la variable "user_body"
    user_body = get_user_body ("Aa")
    # Guardar el resultado de la solicitud para crear a un nuevo usuario en la variable user_response.
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprobar si la respuesta contiene el código de estado 201 mediante assert
    assert user_response.status_code == 201
    # Comprobar si la respuesta contiene el campo authToken y si contiene algunos datos
    assert user_response.json()["authToken"] != ""

    # El resultado de la solicitud de recepción de datos de la tabla "user_model" se guarda en la variable "users_table_response"
    users_table_response = sender_stand_request.get_users_table()
    # El string que debe estar en el cuerpo de la respuesta para recibir datos de la tabla "users" se ve así
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1
    print("Prueba 1 completada con éxito")

# Prueba 2
def test_create_user_15_letter_in_first_name_get_success_response():
    # Preparar los Datos de Entrada (DE)
    user_body = get_user_body("Aaaaaaaaaaaaaaa") # 15 caracteres
    # Acción a realizar (AR): Enviar una solicitud POST al endpoint (?), con el cuerpo que contiene (?)
    user_response = sender_stand_request.post_new_user(user_body)
    # Resultados Esperados (RE): Código de estado 201 y la respuesta debe incluir un campo authToken
    assert user_response.status_code == 201 # Verifica que el codigo de estado es = 201
    assert user_response.json()["authToken"] != "" # Verifica que el authToken no este vacío

# Prueba 3
# Función de prueba negativa
def negative_assert_symbol(first_name):
    # Preparación de los DE (Preparar el cuerpo de la solicitud con el nombre inválido)
    user_body = get_user_body(first_name)
    # Ejecución de las AR (Enviar la solicitud POST para crear un usuario)
    response = sender_stand_request.post_new_user(user_body)
    # Comprobación de los RE
    # Comprobar que el código de estado es 400
    assert response.status_code == 400
    # Comprobar que el atributo "code" es 400
    assert response.json()["code"] == 400
    # Comprobar que el mensaje de error es el correcto
    assert (response.json()["message"] == "Has introducido un nombre de usuario no válido. "\
            "El nombre solo puede contener letras del alfabeto latino, "\
            "la longitud debe ser de 2 a 15 caracteres.")

def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Prueba 4. Error
# El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Prueba 5. Error
# El parámetro "firstName" contiene palabras con espacios
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")

# Prueba 6. Error
# El parámetro "firstName" contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Test 7. Error
# El parámetro "firstName" contiene un string de números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Pruebas 8 y 9. Preparación
# Función de prueba negativa
# La respuesta contiene el siguiente mensaje de error: "No se han enviado todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    # Guarda el resultado de llamar a la función a la variable "response"
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si la respuesta contiene el código 400
    assert response.status_code == 400

    # Comprueba si el atributo "code" en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400

    # Comprueba si el atributo "message" en el cuerpo de respuesta se ve así:
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"

# Prueba 8. Error
# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 10. Error
# El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400












## Código Completo del Proyecto
import sender_stand_request
import data

# Función para cambiar el valor del parámetro firstName en el cuerpo de la solicitud
def get_user_body(first_name):
    # Copiar el diccionario con el cuerpo de la solicitud desde el archivo de datos
    current_body = data.user_body.copy()
    # Se cambia el valor del parámetro firstName
    current_body["firstName"] = first_name
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

# Función de prueba positiva
def positive_assert(first_name):
    # El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body(first_name)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    user_response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # Comprueba que el campo authToken está en la respuesta y contiene un valor
    assert user_response.json()["authToken"] != ""

    # Comprobar que el resultado de la solicitud se guarda en users_table_response
    users_table_response = sender_stand_request.get_users_table()

    # String que debe estar en el cuerpo de respuesta
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Comprueba si el usuario o usuaria existe y es único/a
    assert users_table_response.text.count(str_user) == 1

# Función de prueba negativa para los casos en los que la solicitud devuelve un error relacionado con caracteres
def negative_assert_symbol(first_name):
    # El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body(first_name)

    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 400
    assert response.status_code == 400

    # Comprueba que el atributo code en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba el atributo message en el cuerpo de respuesta
    assert response.json()["message"] == "El nombre que ingresaste es incorrecto. " \
                                         "Los nombres solo pueden contener caracteres latinos,  "\
                                         "los nombres deben tener al menos 2 caracteres y no más de 15 caracteres"

# Función de prueba negativa cuando el error es "No se enviaron todos los parámetros requeridos"
def negative_assert_no_firstname(user_body):
    # El resultado se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprueba si el código de estado es 400
    assert response.status_code == 400

    # Comprueba que el atributo code en el cuerpo de respuesta es 400
    assert response.json()["code"] == 400
    # Comprueba el atributo message en el cuerpo de respuesta
    assert response.json()["message"] == "No se enviaron todos los parámetros requeridos"

# Prueba 1. Usuario o usuaria creada con éxito. El parámetro firstName contiene 2 caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Prueba 2. Usuario o usuaria creada con éxito. El parámetro firstName contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

# Prueba 3. Error. El parámetro firstName contiene 1 carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Prueba 4. Error. El parámetro firstName contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")

# Prueba 5. Usuario o usuaria creada con éxito. El parámetro firstName contiene caracteres latinos
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Prueba 6. Error. El parámetro firstName contiene un string de caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")

# Prueba 7. Error. El parámetro firstName contiene un string de dígitos
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Prueba 8. Error. Falta el parámetro firstName en la solicitud
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    user_body = data.user_body.copy()
    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

# Prueba 9. Error. El parámetro contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body("")
    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)

# Prueba 10. Error. El tipo del parámetro firstName: número
def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo actualizado de la solicitud se guarda en la variable user_body
    user_body = get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400


