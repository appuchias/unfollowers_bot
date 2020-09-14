import os
import sys
from dotenv import load_dotenv

# Main function
def main():
    """Main function"""
    if not os.path.exists("./files/"):
        os.mkdir("files")

    if not os.path.exists(".env"):
        login = input("Login username:\n> ")
        pwd = input("Login password:\n> ")
        uname = input("Username to track:\n> ")

        with open(".env", "w") as w:
            w.write("LOGIN={}\nPASSWORD={}\nUSERNAME={}".format(login, pwd, uname))

    else:
        load_dotenv()

        login = os.getenv("LOGIN")
        pwd = os.getenv("PASSWORD")
        uname = os.getenv("USERNAME")

        print(
            "What do you want to modify?\n"
            + "  [1] - Login username\n"
            + "  [2] - Login password\n"
            + "  [3] - Username to track\n\n"
            + "  [Press CTRL+C to exit]"
        )
        try:
            selection = int(input("> "))
        except KeyboardInterrupt:
            print("\n\n  --Exited--\n")
            sys.exit(0)
        except ValueError:
            print("Uhm, you were asked to enter a number or to exit, not that :/")
            sys.exit(0)

        if selection == 1:
            login = input("Login username:\n> ")
        elif selection == 2:
            pwd = input("Login password:\n> ")
        elif selection == 3:
            uname = input("Username to track:\n> ")
        else:
            print("Please input a number between 1-3")
            sys.exit(0)

        with open(".env", "w") as w:
            w.write("LOGIN={}\nPASSWORD={}\nUSERNAME={}".format(login, pwd, uname))
    print("Done :)")


if __name__ == "__main__":
    main()
