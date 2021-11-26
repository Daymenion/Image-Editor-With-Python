from tkinter import Toplevel, Button, RIGHT
import numpy as np
import cv2
from PIL import Image
from PIL.ImageFilter import (
    CONTOUR, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES
)


class FilteringTopLevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.negative_button = Button(master=self, text="Negative")
        self.black_white_button = Button(master=self, text="Black White")
        self.sepia_button = Button(master=self, text="Sepia")
        self.emboss_button = Button(master=self, text="Emboss")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.median_blur_button = Button(master=self, text="Median Blur")
        self.edges_button = Button(master=self, text="Edges of Photo")
        self.foilPic_button = Button(master=self, text="Foil Art")
        self.pencilPic_button = Button(master=self, text="Sharp Paint")
        self.oilPic_button = Button(master=self, text="Oil Paint")
        self.sketchPic_button = Button(master=self, text="Sketch Light")
        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.negative_button.bind("<ButtonRelease>", self.negative_button_released)
        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.sepia_button.bind("<ButtonRelease>", self.sepia_button_released)
        self.emboss_button.bind("<ButtonRelease>", self.emboss_button_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.gaussian_blur_button_released)
        self.median_blur_button.bind("<ButtonRelease>", self.median_blur_button_released)
        self.edges_button.bind("<ButtonRelease>", self.edges_button_released)
        self.foilPic_button.bind("<ButtonRelease>", self.foilPic_button_released)
        self.pencilPic_button.bind("<ButtonRelease>", self.pencilPic_button_released)
        self.oilPic_button.bind("<ButtonRelease>", self.oilPic_button_released)
        self.sketchPic_button.bind("<ButtonRelease>", self.sketchPic_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.negative_button.pack()
        self.black_white_button.pack()
        self.sepia_button.pack()
        self.emboss_button.pack()
        self.gaussian_blur_button.pack()
        self.median_blur_button.pack()
        self.edges_button.pack()
        self.foilPic_button.pack()
        self.pencilPic_button.pack()
        self.oilPic_button.pack()
        self.sketchPic_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()

    def negative_button_released(self, event):
        self.negative()
        self.show_image()

    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def sepia_button_released(self, event):
        self.sepia()
        self.show_image()

    def emboss_button_released(self, event):
        self.emboss()
        self.show_image()

    def gaussian_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def median_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def edges_button_released(self, event):
        self.edges()
        self.show_image()

    def foilPic_button_released(self, event):
        self.foilPic()
        self.show_image()

    def pencilPic_button_released(self, event):
        self.pencilPic()
        self.show_image()

    def oilPic_button_released(self, event):
        self.oilPic()
        self.show_image()

    def sketchPic_button_released(self, event):
        self.sketchPic()
        self.show_image()

    def apply_button_released(self, event):
        self.master.image_cache.append(self.master.processed_image.copy())
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.interface_functions.show_image()
        self.close()

    def show_image(self):
        self.master.interface_functions.show_image(image=self.filtered_image)

    def negative(self):
        self.filtered_image = cv2.bitwise_not(self.original_image)

    def black_white(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2RGB)

    def sepia(self):
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def emboss(self):
        kernel = np.array([[0, -1, -1],
                           [1, 0, -1],
                           [1, 1, 0]])

        self.filtered_image = cv2.filter2D(self.original_image, -1, kernel)

    def gaussian_blur(self):
        self.filtered_image = cv2.GaussianBlur(self.original_image, (41, 41), 0)

    def median_blur(self):
        self.filtered_image = cv2.medianBlur(self.original_image, 41)

    def edges(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(FIND_EDGES))

    def foilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EMBOSS))

    def pencilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EDGE_ENHANCE_MORE))

    def oilPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(EDGE_ENHANCE))

    def sketchPic(self):
        self.filtered_image = np.array(Image.fromarray(self.original_image).filter(CONTOUR))

    def close(self):
        self.destroy()
