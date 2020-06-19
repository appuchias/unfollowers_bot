from tkinter import Tk, Frame, Label, N
from PIL import Image, ImageTk
import requests

class Interface():
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.bg = "#6f686a"

    def run(self):
        self.window = Tk()
        self.window.title("Instagram unfollower alert bot")
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)
        
        cabecera = Frame(self.window, width=self.width, height=50, bg=self.bg)
        cabecera.pack_propagate(0)
        
        titulo = Label(cabecera, text="Instagram unfollower alert bot", font=("Verdana", 20), bg=self.bg, fg="white")
        cabecera.place(x=0, y=0)
        titulo.pack()
        self.window.mainloop()

    def get_followers(self, followers:list):
        for follower in followers:
            with open(f'thumbnails\{follower.username}.jpg', 'wb') as handle:
                response = requests.get(follower.get_profile_picture_url(), stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

            handle.write(block)
    
    def get_unfollowers(self, unfollowers:list):
        for unfollower in unfollowers:
            with open(f'thumbnails\{unfollower.username}.jpg', 'wb') as handle:
                response = requests.get(
                    unfollower.get_profile_picture_url(), stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

            handle.write(block)

Interface().run()
