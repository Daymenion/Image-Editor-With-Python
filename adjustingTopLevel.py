from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL
import cv2
import numpy as np


class AdjustingTopLevel(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master, width=255, height=765)

        self.isGetApplied = False
        self.morphologyDict = {
            "isGetHistogram": [False, self.histogram_button_released],
            "isGetErosion": [False, True, cv2.MORPH_ERODE],
            "isGetDilation": [False, True, cv2.MORPH_DILATE],
            "isGetOpen": [False, True, cv2.MORPH_OPEN],
            "isGetClose": [False, True, cv2.MORPH_CLOSE],
            "isGetGradient": [False, True, cv2.MORPH_GRADIENT],
            "isGetTopHat": [False, True, cv2.MORPH_TOPHAT],
            "isGetBlackHat": [False, True, cv2.MORPH_BLACKHAT],
            "isGetEllipse": [False, True, cv2.MORPH_ELLIPSE],
            "isGetRect": [False, True, cv2.MORPH_RECT],
            "isGetCross": [False, True, cv2.MORPH_CROSS],
            "isGetLogged": [False, self.log_button_released],
            "isGetPowerLaw": [False, self.power_law_button_released]
        }
        self.brightness_value = 0
        self.previous_brightness_value = 0

        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image
        height, width, channels = self.processing_image.shape
        self.brightness_label = Label(self, text="Brightness Scale")
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                      orient=HORIZONTAL)
        self.r_label = Label(self, text="Red Scale")
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.g_label = Label(self, text="Green Scale")
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.b_label = Label(self, text="Blue Scale")
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                             orient=HORIZONTAL)
        self.kernelSize_label = Label(self, text="Kernel Grid Size")
        self.kernelSize_scale = Scale(self, from_=1, to_=np.gcd(width, height), length=250, resolution=1,
                                      orient=HORIZONTAL)
        self.gammaSize_label = Label(self, text="Gamma Size")
        self.gammaSize_scale = Scale(self, from_=0.1, to_=10.0, length=250, resolution=0.1,
                                     orient=HORIZONTAL)
        self.clipLimitSize_label = Label(self, text="Clip Limit Size")
        self.clipLimitSize_scale = Scale(self, from_=2.0, to_=15.0, length=250, resolution=0.1,
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
        self.log_button = Button(self, text="Log Transformation", width=20, font="ariel 11 bold")
        self.power_law_button = Button(self, text="Power-Law (Gamma)", width=20, font="ariel 11 bold")
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")
        self.clear_button = Button(self, text="Clear")
        self.brightness_scale.set(1)
        self.kernelSize_scale.set(8)
        self.gammaSize_scale.set(0.5)
        self.clipLimitSize_scale.set(2.0)

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
        self.log_button.bind("<ButtonRelease>", self.log_button_released)
        self.power_law_button.bind("<ButtonRelease>", self.power_law_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.preview_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        self.brightness_label.place(x=95, y=0)
        self.brightness_scale.place(x=0, y=20)
        self.r_label.place(x=100, y=60)
        self.r_scale.place(x=0, y=80)
        self.g_label.place(x=100, y=120)
        self.g_scale.place(x=0, y=140)
        self.b_label.place(x=100, y=180)
        self.b_scale.place(x=0, y=200)
        self.kernelSize_label.place(x=90, y=240)
        self.kernelSize_scale.place(x=0, y=255)
        self.erosion_button.place(x=0, y=300)
        self.dilation_button.place(x=120, y=300)
        self.opening_button.place(x=0, y=340)
        self.closing_button.place(x=120, y=340)
        self.gradient_button.place(x=0, y=380)
        self.topHat_button.place(x=120, y=380)
        self.blackHat_button.place(x=0, y=420)
        self.ellipse_button.place(x=120, y=420)
        self.rect_button.place(x=0, y=460)
        self.cross_button.place(x=120, y=460)
        self.log_button.place(x=20, y=500)
        self.clipLimitSize_label.place(x=90, y=540)
        self.clipLimitSize_scale.place(x=0, y=560)
        self.histogram_button.place(x=20, y=600)
        self.gammaSize_label.place(x=95, y=640)
        self.gammaSize_scale.place(x=0, y=660)
        self.power_law_button.place(x=20, y=700)
        self.cancel_button.place(x=0, y=740)
        self.clear_button.place(x=90, y=740)
        self.preview_button.place(x=140, y=740)
        self.apply_button.place(x=200, y=740)

    def histogram_button_released(self, event):
        self.morphologyDict["isGetHistogram"][0] = True
        ycrcb_img = cv2.cvtColor(self.processing_image, cv2.COLOR_RGB2YCrCb)
        ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])

        clahe = cv2.createCLAHE(clipLimit=float(self.clipLimitSize_scale.get()),
                                tileGridSize=(int(self.kernelSize_scale.get()), int(self.kernelSize_scale.get())))
        ycrcb_img[:, :, 0] = clahe.apply(ycrcb_img[:, :, 0])
        self.processing_image = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2RGB)

    def get_kernel(self, morph_name):
        kernel = None
        size = int(self.kernelSize_scale.get())

        try:
            kernel = cv2.getStructuringElement(shape=self.morphologyDict[morph_name][2], ksize=(size, size))
        except cv2.error:
            kernel = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(size, size))
        finally:
            return kernel

    def erosion_button_released(self, event):
        self.morphologyDict["isGetErosion"][0] = True

    def dilation_button_released(self, event):
        self.morphologyDict["isGetDilation"][0] = True

    def opening_button_released(self, event):
        self.morphologyDict["isGetOpen"][0] = True

    def closing_button_released(self, event):
        self.morphologyDict["isGetClose"][0] = True

    def gradient_button_released(self, event):
        self.morphologyDict["isGetGradient"][0] = True

    def topHat_button_released(self, event):
        self.morphologyDict["isGetTopHat"][0] = True

    def blackHat_button_released(self, event):
        self.morphologyDict["isGetBlackHat"][0] = True

    def ellipse_button_released(self, event):
        self.morphologyDict["isGetEllipse"][0] = True

    def rect_button_released(self, event):
        self.morphologyDict["isGetRect"][0] = True

    def cross_button_released(self, event):
        self.morphologyDict["isGetCross"][0] = True

    def log_button_released(self, event):
        self.morphologyDict["isGetLogged"][0] = True
        c = 255 / (np.log(1 + np.max(self.processing_image)))
        log_transformed = c * np.log(1 + self.processing_image)

        self.processing_image = np.array(log_transformed, dtype=np.uint8)

    def power_law_button_released(self, event):
        self.morphologyDict["isGetPowerLaw"][0] = True
        self.processing_image = np.array(255 * (self.processing_image / 255) ** float(self.gammaSize_scale.get()),
                                         dtype='uint8')

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

        for key, value in self.morphologyDict.items():
            if value[0]:
                if value[1] is True:
                    self.processing_image = cv2.morphologyEx(self.processing_image, value[2], self.get_kernel(key))
                else:
                    value[1](event)
        self.show_image(self.processing_image)
        self.isGetApplied = True

    def apply_button_released(self, event):
        if not self.isGetApplied:
            self.preview_button_released(event)
        self.master.image_cache.append(self.master.processed_image.copy())
        self.master.processed_image = self.processing_image
        self.close(event)

    def cancel_button_released(self, event):
        self.close(event)

    def show_image(self, img=None):
        self.master.interface_functions.show_image(image=img)

    def clear_button_released(self, event):
        for values in self.morphologyDict.values():
            values[0] = False
        self.b_scale.set(0)
        self.r_scale.set(0)
        self.g_scale.set(0)
        self.brightness_scale.set(1.0)
        self.kernelSize_scale.set(8)
        self.gammaSize_scale.set(0.5)
        self.clipLimitSize_scale.set(2.0)
        self.processing_image = self.original_image.copy()
        self.show_image(self.processing_image)

    def close(self, event):
        self.show_image()
        self.destroy()
