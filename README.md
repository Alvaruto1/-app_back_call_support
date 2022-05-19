# Aplicación App Call Support
Herramienta para optimizar las llamadas de soporte. Tiene las siguientes funcionalidades
* Sistema de login(inicio de sesión y registro de empleados)
* Modulo de empleados (CRUD)
* Modulo de clientes (CRUD)
* Modulo de registro de llamadas (en construcción)
* Descarga en csv de clientes, empleado y registro de llamadas
## Backend
API implementada con python version 3.8.3 y como microframework flask version 2.1.2. Como base de datos se usa sqlite. Se utlizaron las siguientes librerias:
|Libreria | Version |
| ------ | ------ |
| flask | 2.1.2 |
| flask-sqlalchemy | 2.5.1 |
| flask-cors | 3.0.10 |
| flask-login | 0.6.1 |
| pandas | 1.4.2 |
| Flask-JWT-Extended | 4.4.0 |
### Guia de implementación
#### Ambiente de producción
1. Instalar python version 3.83 y pip
2. Instalación de librerias
```sh
pip install -r requirements.txt
```
3. Creación de base de datos sqlite
```sh
python create_db.py
```
5. Alimentar base de datos (categorias, roles y tipos de documentos)
```sh
python seeds.py
```
4. Correr la API
```sh
flask run
```
### Endpoints
|Endpoint                         |Metodo   |Regla                                                                |Descripción
|-------------------------------  |-------  |-------------------------------------------------------------------- |---------------------------  
|auth.delete_user                 |DELETE   |/users/\<int: type_document_id\>/\<int: user_id\>			  |Borrar usuario por tipo de documento y id
|auth.download_info_user_csv      |GET      |/users/download/\<int: type_document_id\>/\<int: user_id\>		  |Descargar csv de usuario por tipo documento y id
|auth.download_info_users_csv     |GET      |/users/download/							  |Descargar csv de usuarios
|auth.download_info_users_csv     |GET      |/users/download/\<user_type\>					  |Descargar csv de usuario por tipo de usuario (rol)
|auth.get_user_by_document        |GET      |/users/search/\<int: type_document_id\>/\<int: user_id\>		  |Obtener la info de un usuario por tipo de documento y id
|auth.get_users                   |GET      |/users/\<user_type\>						  |Obenter usuarios por tipo de usario(rol)
|auth.logged_in                   |GET      |/logged_in								  |Verificar si se encuetra logueado
|auth.login                       |POST     |/login								  |Iniciar sesión como empleado
|auth.signup                      |POST     |/signup	  							  |Registrarse como empleado
|auth.update_user                 |PUT      |/users/\<int: type_document_id\>/\<int: user_id\>			  |Actualizar usuario
|call_log.create_call_log         |POST     |/call_logs								  |Crear un registro de llamada
|call_log.delete_call_log         |DELETE   |/call_logs/\<int: id\>						  |Borrar un registro de llamada
|call_log.download_call_logs_csv  |GET      |/call_logs/download/\<user_type\>/\<int: document_type_id\>/\<int: id_user\>|Descargar csv en donde se relaciones los registros de llamadas de un usuario y su rol     
|call_log.download_call_logs_csv  |GET      |/call_logs/download/\<user_type\>					  |Descarga csv de registro de llamadas
|call_log.get_call_logs           |GET      |/call_logs/\<user_type\>/\<int: document_type_id\>/\<int: id_user\>  |Obetener los registros de llamadas de un usuario y su rol  
|call_log.get_call_logs           |GET      |/call_logs/\<user_type\>						  |Obetener registros de llamadas
|call_log.update_call_log         |PUT      |/call_logs/\<int: id\>						  |Actualizar un registro de llamada
