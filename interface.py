from tkinter import Frame, Button, Label, Entry, filedialog
from filteringFrame import FilteringFrame
from adjustingFrame import AdjustingFrame
from edgeDetectionFrame import EdgeDetectionFrame
from creditsFrame import CreditsFrame
from PIL import Image
import numpy as np
import cv2


class Interface(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg='gray', width=1280, height=100)

        self.pasted = False

        self.new_button = Button(self, text="New", bg='gold', fg='black', width=10, font="ariel 13 bold")
        self.save_button = Button(self, text="Save", bg='black', fg='gold', width=10, font="ariel 13 bold")
        self.save_as_button = Button(self, text="Save As", bg="magenta", fg='yellow', width=10, font="ariel 13 bold")
        self.filter_button = Button(self, text="Filter", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.adjust_button = Button(self, text="Adjust", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.clear_button = Button(self, text="Clear", bg="cyan", fg='red', width=10, font="ariel 13 bold")
        self.videoProcess_button = Button(self, text="Shape Detection on Webcam", bg="black", fg='red', width=25,
                                          font="ariel 13 bold")
        self.draw_button = Button(self, text="Draw", bg="black", fg='white', width=5, font="ariel 8 bold")
        self.drawClear_button = Button(self, text="Clear Draw", bg="black", fg='white', width=10, font="ariel 8 bold")
        self.crop_button = Button(self, text="Crop", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.rotate_button = Button(self, text="Rotate", bg="black", fg='white', width=5, font="ariel 10 bold")
        self.saveRotation_button = Button(self, text="Save\nRotation", bg="black", fg='white', width=8,
                                          font="ariel 8 bold")
        self.rotate_label = Label(text="Enter Rotate Angle", font="Arial 8 bold")
        self.rotate_entry = Entry(width=15)
        self.resize_button = Button(self, text="Resize", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.resize_label = Label(text="Enter X and Y size", font="Arial 8 bold")
        self.resizeX_entry = Entry(width=8)
        self.resizeY_entry = Entry(width=8)
        self.addMoreImage_button = Button(self, text="Add More Images\nTo Paste Over\nThe First Image",
                                          bg='red', fg='blue', width=15, font="ariel 13 bold")
        self.flip_button = Button(self, text="Flipping", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.contrast_button = Button(self, text="Increase\nContrast", bg="black", fg='white', width=10, font="ariel 13 bold")
        self.credits_button = Button(self, text="Credits", bg="black", fg='gold', width=21, font="ariel 15 bold")

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)
        self.videoProcess_button.bind("<ButtonRelease>", self.videoProcess_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.drawClear_button.bind("<ButtonRelease>", self.drawClear_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.rotate_button.bind("<ButtonRelease>", self.rotate_button_released)
        self.saveRotation_button.bind("<ButtonRelease>", self.saveRotation_button_released)
        self.resize_button.bind("<ButtonRelease>", self.resize_button_released)
        self.addMoreImage_button.bind("<ButtonRelease>", self.addMoreImage_button_released)
        self.flip_button.bind("<ButtonRelease>", self.flip_button_released)
        self.contrast_button.bind("<ButtonRelease>", self.contrast_button_released)
        self.credits_button.bind("<ButtonRelease>", self.credits_button_released)

        self.new_button.place(x=0, y=0)
        self.save_button.place(x=0, y=45)
        self.save_as_button.place(x=120, y=45)
        self.clear_button.place(x=120, y=0)
        self.filter_button.place(x=240, y=0)
        self.adjust_button.place(x=240, y=45)
        self.videoProcess_button.place(x=1020, y=10)
        self.draw_button.place(x=355)
        self.drawClear_button.place(x=405)
        self.crop_button.place(x=360, y=45)
        self.rotate_label.place(x=490)
        self.rotate_entry.place(x=490, y=25)
        self.rotate_button.place(x=475, y=45)
        self.saveRotation_button.place(x=525, y=45)
        self.resize_label.place(x=608)
        self.resizeX_entry.place(x=600, y=25)
        self.resizeY_entry.place(x=660, y=25)
        self.resize_button.place(x=600, y=45)
        self.addMoreImage_button.place(x=720)
        self.flip_button.place(x=885)
        self.contrast_button.place(x=885, y=45)
        self.credits_button.place(x=1020, y=45)

    def checkStatus(self):
        if self.master.is_image_selected:
            if self.master.is_crop_state:
                self.master.interface_functions.deactivate_crop()
            if self.master.is_draw_state:
                self.master.interface_functions.deactivate_draw()
            if self.master.is_paste_state:
                self.master.interface_functions.deactivate_paste()
            else:
                return True
        return False

    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.interface_functions.deactivate_draw()
            if self.master.is_crop_state:
                self.master.interface_functions.deactivate_crop()

            filename = filedialog.askopenfilename()
            image = cv2.cvtColor(np.array(Image.open(filename)), cv2.COLOR_BGR2RGB)

            if image is not None:
                self.master.filename = filename
                self.master.original_image = image.copy()
                self.master.processed_image = image.copy()
                self.master.interface_functions.show_image()
                self.master.is_image_selected = True
                self.master.num_rows, self.master.num_cols = self.master.processed_image.shape[:2]

    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.checkStatus():
                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)

    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.checkStatus():
                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename()
                filename = filename + "." + original_file_type

                save_image = self.master.processed_image
                cv2.imwrite(filename, save_image)

                self.master.filename = filename

    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if self.checkStatus():
                self.master.filtering_frame = FilteringFrame(master=self.master)
                self.master.filtering_frame.grab_set()

    def adjust_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.checkStatus():
                self.master.adjusting_frame = AdjustingFrame(master=self.master)
                self.master.adjusting_frame.grab_set()

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.checkStatus():
                self.master.processed_image = self.master.original_image.copy()
                self.master.interface_functions.show_image()

    def videoProcess_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.videoProcess_button:
            if self.checkStatus():
                print("There will be the amount of area and the approximate number of "
                      "edges of the objects detected by the camera in console.")

            self.master.edgeDetection_frame = EdgeDetectionFrame(master=self.master)
            self.master.edgeDetection_frame.grab_set()

    def draw_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.checkStatus():
                self.master.interface_functions.activate_draw()

    def drawClear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.drawClear_button:
            self.master.interface_functions.clear_draw()

    def crop_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.checkStatus():
                self.master.interface_functions.activate_crop()

    def rotate_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.rotate_button:
            if self.checkStatus():
                self.master.interface_functions.rotate(float(self.rotate_entry.get()))

    def saveRotation_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.saveRotation_button:
            if self.checkStatus():
                self.master.processed_image = self.master.rotating_image

    def resize_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.resize_button:
            if self.checkStatus():
                self.master.interface_functions.resizing(int(self.resizeX_entry.get()), int(self.resizeY_entry.get()))

    def addMoreImage_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.addMoreImage_button:
            if self.checkStatus():
                filename = filedialog.askopenfilename()
                image = cv2.cvtColor(np.array(Image.open(filename)), cv2.COLOR_BGRA2RGBA)

                if image is not None:
                    self.master.more_imageFilename = filename
                    self.master.more_image = image.copy()
                    self.master.interface_functions.activate_paste()

    def flip_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.flip_button:
            if self.checkStatus():
                self.master.interface_functions.flipping()

    def contrast_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.contrast_button:
            if self.checkStatus():
                self.master.interface_functions.contrast()

    def credits_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.credits_button:
            self.master.credits_frame = CreditsFrame(master=self.master)
            self.master.credits_frame.grab_set()