import json, os

os.system("mkdir files")

try:
    with open("filescredenciales.json", "r+") as r:
        if len(r.read()) > 2:
            print("El archivo con las credenciales ya existe. Los cambios sobreescribirán lo guardado anteriormente")
        else:
            r.write("{}")
except:
    file = open("files/credenciales.json", "w")
    file.write("{}")
    file.close()

with open("files/credenciales.json") as r:
    credentials = json.load(r)

credentials["login_username"] = input(
    "Nombre de usuario de la cuenta secundaria:\n> ")
credentials["login_password"] = input(
    "Contraseña de la cuenta secundaria:\n> ")
credentials["username"] = input(
    "Cuenta de la que revisar los seguidores:\n> ")

with open("files/credenciales.json", "w") as w:
    json.dump(credentials, w, indent=4)
