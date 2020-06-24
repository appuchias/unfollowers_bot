from igramscraper.exception.instagram_auth_exception import InstagramAuthException
from igramscraper.instagram import Instagram
from win10toast import ToastNotifier
import json, threading, tray_icon
from time import sleep

toaster = ToastNotifier()

delay_mins = 40

# Get the credentials and username of the account to track
try:
    with open("files/credenciales.json", "r") as r:
        credentials = json.load(r)
        login_username = credentials["login_username"]
        login_password = credentials["login_password"]
        username = credentials["username"]
except:
    toaster.show_toast("Error!", "Ejecuta setup_file.py antes de main! (credenciales.json no existe)")

assert len(login_username) or len(login_password) or len(username), "Error obteniendo las credenciales del archivo"

# Instagram related stuff
ig = Instagram()
ig.with_credentials(login_username, login_password)
ig.login()
account = ig.get_account(username)

# Checker function
def get_updates(account):
    try:
        followers = ig.get_followers(account.identifier, 150, 100, delayed=True)["accounts"] # Get all the followers
        followers_usernames = [follower.username for follower in followers]
    except InstagramAuthException:
        toaster.show_toast("Error!", "Demasiadas peticiones! Espera antes de reintentarlo")

    try:
        with open("files/followers.txt") as r:
            users = [user.strip(" '") for user in r.read().strip("[]").split("', '")]
    except FileNotFoundError:
        users = []

    new_followers = []
    new_unfollowers = []

    if len(users) > 1:
        for follower in followers:
            if follower.username not in users:
                new_followers.append(follower)
                toaster.show_toast("New follower:", follower.username)

        for user in users:
            if user not in followers_usernames:
                new_unfollowers.append(follower)
                toaster.show_toast("New unfollower:", user)

    with open("files/followers.txt", "w") as w:
        w.write(str(followers_usernames))

    try:
        file = open("files/recents.txt", "a")
        file.close()
    except FileNotFoundError:
        file = open("files/recents.txt", "x")
        file.close()
    finally:
        with open("files/recents.txt", "a") as a:
            if len(new_followers) >= 1:
                a.write("\n" + str([follower.username for follower in new_followers]).replace("[", "").replace("]", ""))
            else:
                a.write("\nNinguno")

            if len(new_unfollowers) >= 1:
                a.write("\n" + str([unfollower.username for unfollower in new_unfollowers]).replace("[", "").replace("]", ""))
            else:
                a.write("\nNinguno")

while True:
    get_updates(account)
    sleep(delay_mins*60)
