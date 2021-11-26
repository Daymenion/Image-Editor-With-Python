from tkinter import Toplevel, RIGHT, LEFT, Label, Scale, Button, HORIZONTAL, CENTER
import cv2
import numpy as np


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                         scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        ver = np.hstack(imgArray)
    return ver


class EdgeDetectionTopLevel(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.finished = False
        self.images = None
        self.cap = None

        self.orginal_image = self.master.processed_image

        self.start_button = Button(master=self, text="Open Camera")
        self.finish_button = Button(master=self, text="Finish Process")
        self.wm_title("Edge Detection")
        self.thresholdParam_label = Label(self, text="Threshold Parameter")
        self.thresholdParam_scale = Scale(self, from_=0, to_=255, length=300, resolution=0.1, activebackground="gray",
                                          cursor="arrow", orient=HORIZONTAL)
        self.thresholdParam_scale.set(40)

        self.thresholdParam2_label = Label(self, text="Other Threshold Parameter")
        self.thresholdParam2_scale = Scale(self, from_=0, to_=255, length=300, resolution=0.1, activebackground="gray",
                                           cursor="arrow", orient=HORIZONTAL)

        self.areaParam_label = Label(self, text="Area Parameter")
        self.areaParam_scale = Scale(self, from_=300, to_=10000, length=300, resolution=1, activebackground="gray",
                                     cursor="arrow", orient=HORIZONTAL)

        self.start_button.bind("<ButtonRelease>", self.start_button_released)
        self.finish_button.bind("<ButtonRelease>", self.finish_button_released)

        self.thresholdParam_label.pack()
        self.thresholdParam_scale.pack(anchor=CENTER)
        self.thresholdParam2_label.pack()
        self.thresholdParam2_scale.pack(anchor=CENTER)
        self.areaParam_label.pack()
        self.areaParam_scale.pack()
        self.start_button.pack(side=RIGHT)
        self.finish_button.pack(side=LEFT)

    def start_button_released(self, event):
        self.video_capture()

    def finish_button_released(self, event):
        self.master.interface_functions.clear_canvas()
        if self.master.processed_image is not None:
            self.master.interface_functions.show_image()
        self.finished = True

    def show_image(self):
        self.master.interface_functions.show_image(image=self.images)

    def getContours(self, img, imgContour):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # etrafta çok fazla öge varsa ve en çok alana sahip olanların yakalanmasını istiyorsanız bu yorum satırını açın
        # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
        for cnt in contours:
            area = cv2.contourArea(cnt)
            print(area)
            areaMin = self.areaParam_scale.get()
            if area > areaMin:
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                print(len(approx))
                objCor = len(approx)
                x, y, w, h = cv2.boundingRect(approx)

                if objCor == 3:
                    objectType = "Triangle"
                elif objCor == 4:
                    aspRatio = w / float(h)
                    if 0.98 < aspRatio < 1.03:
                        objectType = "Square"
                    else:
                        objectType = "Rectangle"
                elif objCor > 10:
                    objectType = "Circles"
                else:
                    objectType = "Polygon"

                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(imgContour, objectType,
                            (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 0, 0), 2)
                cv2.putText(imgContour, "Area: " + str(area),
                            (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 0, 0), 2)

    def video_capture(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while True:
            self.update()
            if self.finished:
                self.close()
                break

            success, img = self.cap.read()
            imgContour = img.copy()
            imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
            imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

            threshold1 = self.thresholdParam_scale.get()
            threshold2 = self.thresholdParam2_scale.get()
            imgCanny = cv2.Canny(imgGray, threshold1, threshold2)

            kernel = np.ones((5, 5))
            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

            self.getContours(imgDil, imgContour)

            self.images = stackImages(0.8, ([img, imgGray, imgCanny],
                                            [imgDil, imgContour, imgContour]))

            self.show_image()
            self.master.update()

    def close(self):
        self.cap.release()
        self.destroy()
