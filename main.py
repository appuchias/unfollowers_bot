from igramscraper.exception.instagram_auth_exception import InstagramAuthException
from igramscraper.instagram import Instagram
import json, keyboard
import interface

try:
    with open("credentials.json", "r") as r:
        credentials = json.load(r)
        login_username = credentials["login_username"]
        login_password = credentials["login_password"]
        username = credentials["username"]
except:
    print("Run setup_file.py before running the main file! (credentials.json does not exist)")

assert len(login_username) or len(login_password) or len(username), "Failed to get credentials from file"

ig = Instagram()
ig.with_credentials(login_username, login_password)
ig.login(force=False)
account = ig.get_account(username)

print(1)

try:
    followers = ig.get_followers(account.identifier, 150, 100, delayed=True)["accounts"]
except InstagramAuthException:
    print("Rate limited! Wait before retrying")

try:
    with open("followers.txt") as r:
        users = [user.strip(" '") for user in r.read().strip("[]").split("', '")]
except FileNotFoundError:
    users = []

new_followers = []
new_unfollowers = []

print(1)

if len(users) > 1:
    for follower in followers:
        if follower.username not in users:
            new_followers.append(follower)

    for user in users:
        if user not in [follower.username for follower in followers]:
            new_unfollowers.append(follower)

print(1)

with open("followers.txt", "w") as w:
    w.write(str(followers))

print(new_followers, new_unfollowers)

print("Program finished")

gui = interface.Interface()
gui.get_followers(new_followers)
gui.get_unfollowers(new_unfollowers)
gui.run()
