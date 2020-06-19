import json

try:
    with open("credentials.json", "r+") as r:
        if len(r.read()) > 2:
            print("Credentials file already exists. Any change will overwrite the previous file")
        else:
            r.write("{}")
except:
    file = open("credentials.json", "w")
    file.write("{}")
    file.close()

with open("credentials.json") as r:
    credentials = json.load(r)

credentials["login_username"] = input(
    "Please input the username used to log into the bot account:\n> ")
credentials["login_password"] = input(
    "Please input the password used to log into the bot account:\n> ")
credentials["username"] = input(
    "Please input the username to track followers from:\n> ")

with open("credentials.json", "w") as w:
    json.dump(credentials, w, indent=4)
