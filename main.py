from igramscraper.exception.instagram_auth_exception import InstagramAuthException
from igramscraper.instagram import Instagram
import os, json

with open("credentials.json", "r") as r:
    credentials = json.load(r)
    login_username = credentials["login_username"]
    login_password = credentials["login_password"]
    username = credentials["username"]

assert len(login_username) or len(login_password) or len(username), "Failed to get credentials from file"

ig = Instagram()
ig.with_credentials(login_username, login_password)
ig.login(force=False)

account = ig.get_account(username)

try:
    followers = [follower.username for follower in ig.get_followers(account.identifier, 150, 100)["accounts"]]
except InstagramAuthException:
    print("Rate limited! Wait before retrying")

try:
    with open("followers.txt") as r:
        users = [user.strip(" '") for user in r.read().strip("[]").split("', '")]
except FileNotFoundError:
    users = []

if len(users) > 1:
    for follower in followers:
        if follower not in users:
            print("New follower! >", follower)

    for user in users:
        if user not in followers:
            print(user, "unfollowed you!")

with open("followers.txt", "w") as w:
    w.write(str(followers))

print("Program finished")
