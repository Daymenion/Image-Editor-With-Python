from tkinter import Toplevel, Canvas, Button, Label, NW
from PIL import ImageTk
import webbrowser


def callback(url):
    webbrowser.open_new(url)


class CreditsTopLevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, bg='gray', width=1380, height=700)

        self.canvas = Canvas(self, bg="gray", width=560, height=350)
        self.canvas.place(x=10, y=280)

        self.img = ImageTk.PhotoImage(file="./Sample_Images/LeftHand.png")
        self.canvas.create_image(0, 40, anchor=NW, image=self.img)

        self.canvas2 = Canvas(self, bg="gray", width=560, height=350)
        self.canvas2.place(x=800, y=280)

        self.img2 = ImageTk.PhotoImage(file="./Sample_Images/RightHand.png")
        self.canvas2.create_image(70, 40, anchor=NW, image=self.img2)

        self.general_page = Label(master=self, text="This project offers an application infrastructure"
                                                    " that allows you to edit photos.\n"
                                                    "You can learn more about the project and where in the code"
                                                    " does what by reading the Read.me file.\nRead.me file is in"
                                                    " Turkish, you can translate it to English if you want,\n"
                                                    " Google translate translates the sentences correctly.\n"
                                                    " This code tells you how to manipulate form files in general"
                                                    " terms,\nhow to create form applications in oop structure,\n"
                                                    " how to make edits on the photos and how to transfer these"
                                                    " arrangements to canvas.\n You can learn how to use form files via"
                                                    " python and image editing steps in python using this project.\n"
                                                    "\nCreating by Daymenion\n",
                                  bg="gray", fg="black", font="ariel 15 bold")
        self.instagram_page = Label(master=self, text="My Instagram Page", bg="gray", fg="blue",
                                    font="ariel 15 bold", cursor="hand2")
        self.twitter_page = Label(master=self, text="My Twitter Page", bg="gray", fg="blue",
                                  font="ariel 15 bold", cursor="hand2")
        self.githup_page = Label(master=self, text="My Githup Page", bg="gray", fg="blue",
                                 font="ariel 15 bold", cursor="hand2")
        self.youtube_page = Label(master=self, text="My Youtube Page", bg="gray", fg="blue",
                                  font="ariel 15 bold", cursor="hand2")
        self.linkedin_page = Label(master=self, text="My Linkedin Page", bg="gray", fg="blue",
                                   font="ariel 15 bold", cursor="hand2")
        self.twitch_page = Label(master=self, text="My Twitch Page", bg="gray", fg="blue",
                                 font="ariel 15 bold", cursor="hand2")
        self.discord_page = Label(master=self, text="My Discord Channel", bg="gray", fg="blue",
                                  font="ariel 15 bold", cursor="hand2")
        self.exit_button = Button(self, text="Exit Credits Page", bg="black", fg='white', width=15, font="ariel 13 bold")

        self.twitch_page.bind("<Button-1>", lambda e: callback("https://www.twitch.tv/daymenion"))
        self.discord_page.bind("<Button-1>", lambda e: callback("https://discord.com/invite/XZjnjZHJCB"))
        self.linkedin_page.bind("<Button-1>", lambda e: callback("https://www.linkedin.com/in/daymenion/"))
        self.githup_page.bind("<Button-1>", lambda e: callback("https://github.com/Daymenion"))
        self.instagram_page.bind("<Button-1>", lambda e: callback("https://www.instagram.com/daymenion/"))
        self.youtube_page.bind("<Button-1>", lambda e: callback("https://www.youtube.com/c/Daymenion"))
        self.twitter_page.bind("<Button-1>", lambda e: callback("https://twitter.com/Daymenion"))
        self.exit_button.bind("<ButtonRelease>", self.exit_button_released)

        self.general_page.place(x=250, y=0)
        self.githup_page.place(x=600, y=260)
        self.youtube_page.place(x=600, y=320)
        self.instagram_page.place(x=600, y=380)
        self.twitter_page.place(x=600, y=440)
        self.twitch_page.place(x=600, y=500)
        self.linkedin_page.place(x=600, y=560)
        self.discord_page.place(x=600, y=620)
        self.exit_button.place(x=600, y=650)

        self.mainloop(3)

    def exit_button_released(self, event):
        self.destroy()
