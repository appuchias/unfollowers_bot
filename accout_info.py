from igramscraper.exception.instagram_auth_exception import InstagramAuthException
from igramscraper.instagram import Instagram
import os

password = os.getenv("PASS")

ig = Instagram()
ig.with_credentials('idifjfo_', password)
ig.login(force=False)

username = "alexito.19"

account = ig.get_account(username)

try:
    followers = [follower.username for follower in ig.get_followers(account.identifier, 150, 100, delayed=True)["accounts"]]
except InstagramAuthException:
    print("Rate limited! Wait before retrying")
    

try:
    with open("followers.txt") as r:
        users = [user.strip(" '") for user in r.read().strip("[]").split("', '")]
except FileNotFoundError:
    users = []

for follower in followers:
    if follower not in users:
        print("New follower! >", follower)

for user in users:
    if user not in followers:
        print(user, "unfollowed you!")

with open("followers.txt", "w") as w:
    w.write(str(followers))
