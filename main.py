from igramscraper.exception.instagram_auth_exception import InstagramAuthException
from igramscraper.instagram import Instagram
import json, keyboard
from win10toast import ToastNotifier

delay_mins = 60
run_afk = True

try:
    with open("files/credentials.json", "r") as r:
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
toaster = ToastNotifier()

def get_updates(account):
    try:
        followers = ig.get_followers(account.identifier, 150, 100, delayed=True)["accounts"] # Get all the followers
        followers_usernames = [follower.username for follower in followers]
    except InstagramAuthException:
        print("Rate limited! Wait before retrying")

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

    print([follower.username for follower in new_followers],
        [unfollower.username for unfollower in new_unfollowers])

get_updates(account)
