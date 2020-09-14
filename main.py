from time import sleep
from random import randint
from datetime import datetime
from igramscraper.instagram import Instagram
from igramscraper.exception.instagram_auth_exception import InstagramAuthException

from os import getenv
from dotenv import load_dotenv

load_dotenv()

DELAY = 40  # Cooldown between follower checks in minutes

# Log in function
def login(username):
    ig = Instagram()
    ig.with_credentials(getenv("LOGIN"), getenv("PASSWORD"))
    ig.login()

    print("Logged in")

    sleep(randint(0, 10))

    account = ig.get_account(username)

    return ig, account


# Get followers
def get_followers(ig, account):
    """Get all followers from an account"""

    try:
        followers = ig.get_followers(account.identifier, 2000, 150, delayed=True)[
            "accounts"
        ]
    except InstagramAuthException:
        print("Error. Rate limited. Waiting before retrying...")
        raise SystemExit("Exiting the program...")

    return followers


# Checker function
def main():
    """Main function"""

    ig, account = login(getenv("USERNAME"))

    print("Getting followers")

    followers = get_followers(ig, account)
    followers_usernames = [follower.username for follower in followers]

    print(str(len(followers_usernames)) + " followers")

    try:
        with open("followers.txt", "r") as r:
            users = r.readlines()
    except FileNotFoundError:
        users = []

    unfollowers = []

    print("Getting unfollowers:")

    if users:
        for user in users:
            if user.strip() not in followers_usernames:
                unfollowers.append(user)
                print("  Unfollower: @", user)
    else:
        print("No followers saved. Unfollowers will appear on next check")

    with open("followers.txt", "w") as w:
        w.write("\n".join(followers_usernames))

    with open("unfollowers.txt", "a") as a:
        if unfollowers:
            a.write(str(datetime.now()))
        a.write("\n".join(unfollowers) + "\n")


# Create checker loop
def loop():
    """Just the checker loop function"""

    while True:
        try:
            main()
            true_delay = randint(DELAY - 15, DELAY + 15)
            print(str(datetime.now()) + " -> Current delay: " + str(true_delay) + "min")
            print("---------------------")
            sleep(true_delay * 60)
        except KeyboardInterrupt:
            raise SystemExit("\n\n  --Exited--\n\n")


if __name__ == "__main__":
    loop()
