import json
import os
from time import sleep
from random import randint
from datetime import datetime
from igramscraper.instagram import Instagram
from igramscraper.exception.instagram_auth_exception import InstagramAuthException

from os import getenv  # pylint: disable-msg=C0411
from dotenv import load_dotenv

load_dotenv()

DELAY = 40  # Cooldown between follower checks in minutes

# Get the accounts to track followers
def get_tracker_accounts():
    pass


# Log in function
def login(username, password):
    ig = Instagram()
    ig.with_credentials(username, password)
    ig.login()

    return ig


# Get followers
def get_followers(ig, account):
    """Get all followers from an account"""

    count = (
        int(account.followed_by_count / 100) + (account.followed_by_count % 100 > 0)
    ) * 100
    print(
        "    (Over) estimated "
        + str(count)
        + " followers (~"
        + str(round(count / 10 / 60, 1))
        + " minutes to load)"
    )

    try:
        followers = ig.get_followers(account.identifier, count, 150, delayed=True)
        followers = followers["accounts"]
    except InstagramAuthException:
        raise SystemExit("Rate limited. Exiting the program...")

    return followers


# Checker function
def main(ig, account):
    """Main function"""

    print("  Getting followers")

    followers = get_followers(ig, account)
    followers_usernames = [follower.username for follower in followers]

    try:
        with open("followers.json", "r") as r:
            users = json.load(r)
    except FileNotFoundError:
        users = {"": ["", ""]}

    try:
        with open("unfollowers.json", "r") as r2:
            unfollowers = json.load(r2)
    except FileNotFoundError:
        unfollowers = {"": {"": ["", ""]}}

    # Fill both dictionaries
    try:
        users[account.username]
    except KeyError:
        users[account.username] = []
    try:
        unfollowers[account.username]
    except KeyError:
        unfollowers[account.username] = {}

    # Print followers
    new_followers = []

    for follower in followers_usernames:
        if follower not in [user.strip() for user in users[account.username]]:
            new_followers.append(follower)

    print(
        "    Found "
        + str(len(followers_usernames))
        + " followers -> +"
        + str(len(new_followers))
        + ((" [" + " ".join(new_followers) + "]") if new_followers else "")
    )

    # Get unfollowers
    for user in users[account.username]:
        if user.strip() not in followers_usernames:
            current_time = str(datetime.now())
            unfollowers[account.username][current_time] = []
            unfollowers[account.username][current_time].append(user)
            print("    Unfollower -> @" + user)

    # Write save files
    with open("followers.json", "w") as w:
        users[account.username] = followers_usernames
        json.dump(users, w, indent=4)

    with open("unfollowers.json", "w") as w2:
        json.dump(unfollowers, w2, indent=4)


# Create checker loop
def loop():
    """Just the checker loop function"""

    check = 0

    print("Starting up...")
    ig = login(getenv("LOGIN"), getenv("PASSWORD"))

    sleep(randint(1, 10))
    os.system("cls" if os.name == "nt" else "clear")

    while True:

        check += 1

        try:

            with open("usernames.txt", "r") as r:
                usernames = r.readlines()

            print("Check #" + str(check))
            print("-" * 26)  # ----------
            print(str(datetime.now()) + "\n")

            for username in usernames:
                print("@" + username.strip())
                account = ig.get_account(username.strip())
                main(ig, account)
                print("*-* " * 10)  # *-* *-* *-*

            true_delay = randint(DELAY - 10, DELAY + 10)
            print("Delay: " + str(true_delay) + "min\n")
            sleep(true_delay * 60)  # Transfer to seconds

        except KeyboardInterrupt:
            raise SystemExit("\n\n  --Exited--\n\n")
        except InstagramAuthException:
            raise SystemExit("\n\n  --Instagram error--\n\n")


if __name__ == "__main__":
    loop()
