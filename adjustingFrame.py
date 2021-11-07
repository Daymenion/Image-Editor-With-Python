from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT, TOP, LEFT
import cv2


class AdjustingFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.morphologyDict = {
            "isGetHistogram": [False, self.histogram_button_released],
            "isGetErosion": [False, self.erosion_button_released, cv2.MORPH_ERODE],
            "isGetApplied": [False, self.apply_button_released],
            "isGetDilation": [False, self.dilation_button_released, cv2.MORPH_DILATE],
            "isGetOpen": [False, self.opening_button_released, cv2.MORPH_OPEN],
            "isGetClose": [False, self.closing_button_released, cv2.MORPH_CLOSE],
            "isGetGradient": [False, self.gradient_button_released, cv2.MORPH_GRADIENT],
            "isGetTopHat": [False, self.topHat_button_released, cv2.MORPH_TOPHAT],
            "isGetBlackHat": [False, self.blackHat_button_released, cv2.MORPH_BLACKHAT],
            "isGetEllipse": [False, self.ellipse_button_released, cv2.MORPH_ELLIPSE],
            "isGetRect": [False, self.rect_button_released, cv2.MORPH_RECT],
            "isGetCross": [False, self.cross_button_released, cv2.MORPH_CROSS]
        }
        self.brightness_value = 0
        self.previous_brightness_value = 0

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        self.brightness_label = Label(self, text="Brightness")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                      orient=HORIZONTAL)
        self.r_label = Label(self, text="R")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.g_label = Label(self, text="G")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="B")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.histogram_button = Button(self, text="Histogram Equalization", width=20, font="ariel 11 bold")
        self.erosion_button = Button(self, text="Erosion", width=10, font="ariel 11 bold")
        self.dilation_button = Button(self, text="Dilation", width=10, font="ariel 11 bold")
        self.opening_button = Button(self, text="Opening", width=10, font="ariel 11 bold")
        self.closing_button = Button(self, text="Closing", width=10, font="ariel 11 bold")
        self.gradient_button = Button(self, text="Gradient", width=10, font="ariel 11 bold")
        self.topHat_button = Button(self, text="Top Hat", width=10, font="ariel 11 bold")
        self.blackHat_button = Button(self, text="Black Hat", width=10, font="ariel 11 bold")
        self.ellipse_button = Button(self, text="Ellipse", width=10, font="ariel 11 bold")
        self.rect_button = Button(self, text="Rect", width=10, font="ariel 11 bold")
        self.cross_button = Button(self, text="Cross", width=10, font="ariel 11 bold")
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")
        self.clear_button = Button(self, text="Clear")
        self.brightness_scale.set(1)

        self.histogram_button.bind("<ButtonRelease>", self.histogram_button_released)
        self.erosion_button.bind("<ButtonRelease>", self.erosion_button_released)
        self.dilation_button.bind("<ButtonRelease>", self.dilation_button_released)
        self.opening_button.bind("<ButtonRelease>", self.opening_button_released)
        self.closing_button.bind("<ButtonRelease>", self.closing_button_released)
        self.gradient_button.bind("<ButtonRelease>", self.gradient_button_released)
        self.topHat_button.bind("<ButtonRelease>", self.topHat_button_released)
        self.blackHat_button.bind("<ButtonRelease>", self.blackHat_button_released)
        self.ellipse_button.bind("<ButtonRelease>", self.ellipse_button_released)
        self.rect_button.bind("<ButtonRelease>", self.rect_button_released)
        self.cross_button.bind("<ButtonRelease>", self.cross_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.preview_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.brightness_label.pack()
        self.brightness_scale.pack()
        self.r_label.pack()
        self.r_scale.pack()
        self.g_label.pack()
        self.g_scale.pack()
        self.b_label.pack()
        self.b_scale.pack()
        self.histogram_button.pack(side=TOP)
        self.erosion_button.pack()
        self.dilation_button.pack()
        self.opening_button.pack()
        self.closing_button.pack()
        self.gradient_button.pack()
        self.topHat_button.pack()
        self.blackHat_button.pack()
        self.ellipse_button.pack()
        self.rect_button.pack()
        self.cross_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.clear_button.pack(side=RIGHT)
        self.preview_button.pack(side=RIGHT)
        self.apply_button.pack(side=LEFT)

    def apply_button_released(self, event):
        if not self.morphologyDict["isGetApplied"][0]:
            self.morphologyDict["isGetApplied"][0] = False
            self.preview_button_released(event)
        self.master.processed_image = self.processing_image
        self.close(event)

    def histogram_button_released(self, event):
        self.morphologyDict["isGetHistogram"][0] = True
        ycrcb_img = cv2.cvtColor(self.processing_image, cv2.COLOR_RGB2YCrCb)
        ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])
        self.processing_image = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2RGB)

    def getKernel(self, morphName):
        kernel = None
        try:
            kernel = cv2.getStructuringElement(shape=self.morphologyDict[morphName][2], ksize=(5, 5))
        except cv2.error:
            kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(5, 5))
        finally:
            return kernel

    def erosion_button_released(self, event):
        self.morphologyDict["isGetErosion"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetErosion"][2],
                                                 self.getKernel("isGetErosion"))

    def dilation_button_released(self, event):
        self.morphologyDict["isGetDilation"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetDilation"][2],
                                                 self.getKernel("isGetDilation"))

    def opening_button_released(self, event):
        self.morphologyDict["isGetOpen"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetOpen"][2],
                                                 self.getKernel("isGetOpen"))

    def closing_button_released(self, event):
        self.morphologyDict["isGetClose"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetClose"][2],
                                                 self.getKernel("isGetClose"))

    def gradient_button_released(self, event):
        self.morphologyDict["isGetGradient"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetGradient"][2],
                                                 self.getKernel("isGetGradient"))

    def topHat_button_released(self, event):
        self.morphologyDict["isGetTopHat"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetTopHat"][2],
                                                 self.getKernel("isGetTopHat"))

    def blackHat_button_released(self, event):
        self.morphologyDict["isGetBlackHat"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetBlackHat"][2],
                                                 self.getKernel("isGetBlackHat"))

    def ellipse_button_released(self, event):
        self.morphologyDict["isGetEllipse"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetEllipse"][2],
                                                 self.getKernel("isGetEllipse"))

    def rect_button_released(self, event):
        self.morphologyDict["isGetRect"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetRect"][2],
                                                 self.getKernel("isGetRect"))

    def cross_button_released(self, event):
        self.morphologyDict["isGetCross"][0] = True
        self.processing_image = cv2.morphologyEx(self.processing_image, self.morphologyDict["isGetCross"][2],
                                                 self.getKernel("isGetCross"))

    def preview_button_released(self, event):
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        b, g, r = cv2.split(self.processing_image)

        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        self.processing_image = cv2.merge((b, g, r))

        for value in self.morphologyDict.values():
            if value[0]:
                value[1](event)
        self.show_image(self.processing_image)
        self.morphologyDict["isGetApplied"][0] = True

    def cancel_button_released(self, event):
        self.close(event)

    def show_image(self, img=None):
        self.master.interface_functions.show_image(img=img)

    def clear_button_released(self, event):
        for values in self.morphologyDict.values():
            values[0] = False
        self.processing_image = self.original_image.copy()
        self.show_image(self.processing_image)

    def close(self, event):
        self.show_image()
        self.destroy()
