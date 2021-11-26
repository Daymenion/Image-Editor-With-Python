from tkinter import Frame, Canvas, CENTER, ROUND
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
import cv2


class InterfaceFunctions(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="black", width=1280, height=720)

        self.shown_image = None
        self.x = 0
        self.y = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.rectangle_id = 0
        self.ratio = 0
        self.rotate_angle = 0
        self.forward_cache = list()

        self.canvas = Canvas(self, bg="black", width=1280, height=720)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_image(self, image=None):
        self.clear_canvas()

        if image is None:
            image = self.master.processed_image.copy()
        else:
            image = image

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))

        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    def contrast(self):
        self.master.image_cache.append(self.master.processed_image.copy())
        contrast = (ImageEnhance.Contrast(Image.fromarray(self.master.processed_image))).enhance(1.1)
        self.master.processed_image = np.array(contrast)
        self.master.image_cache.append(self.master.processed_image.copy())
        self.show_image()

    def flipping(self):
        self.master.image_cache.append(self.master.processed_image.copy())
        flipping_image = Image.fromarray(self.master.processed_image).copy()
        flipping_image = flipping_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.master.processed_image = np.array(flipping_image).copy()
        self.master.image_cache.append(self.master.processed_image.copy())
        self.show_image()

    def resizing(self, x, y):
        if x or y == '':
            x, y = 500, 500
        else:
            x, y = int(x),  int(y)
        self.master.image_cache.append(self.master.processed_image.copy())
        self.master.processed_image = np.array(Image.fromarray(self.master.processed_image).resize((x, y)))
        self.master.image_cache.append(self.master.processed_image.copy())
        self.show_image()

    def rotate(self, rotateAngle):
        if rotateAngle == '':
            rotateAngle = 60
        else:
            float(rotateAngle)
        self.rotate_angle += rotateAngle
        self.master.rotating_image = np.array(Image.fromarray(self.master.processed_image).rotate(self.rotate_angle))
        self.master.image_cache.append(self.master.rotating_image.copy())
        self.show_image(image=self.master.rotating_image)

    def activate_paste(self):
        self.canvas.bind("<ButtonPress>", self.start_paste)
        self.canvas.bind("<B1-Motion>", self.pasting)
        self.canvas.bind("<ButtonRelease>", self.end_paste)

        self.master.is_paste_state = True

    def activate_draw(self):
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.master.is_draw_state = True

    def activate_crop(self):
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)

        self.master.is_crop_state = True

    def deactivate_paste(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")

        self.master.is_paste_state = False

    def deactivate_draw(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")

        self.master.is_draw_state = False

    def deactivate_crop(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")

        self.master.is_crop_state = False

    def start_paste(self, event):
        self.master.image_cache.append(self.master.processed_image.copy())
        self.x = event.x
        self.y = event.y

    def start_draw(self, event):
        self.master.image_cache.append(self.master.processed_image.copy())
        self.x = event.x
        self.y = event.y

    def pasting(self, event):
        global img
        img = ImageTk.PhotoImage(file=self.master.more_imageFilename)
        self.canvas.create_image(self.x, self.y, image=img)
        self.x = event.x
        self.y = event.y

    def end_paste(self, event):
        master_image = Image.fromarray(self.master.processed_image).copy()
        pasting_image = Image.fromarray(self.master.more_image).copy()

        position = (self.x - int(pasting_image.width/2), self.y - int(pasting_image.height/2))
        master_image.paste(pasting_image, position, pasting_image)

        self.master.processed_image = np.array(master_image)
        self.show_image()

    def draw(self, event):
        self.canvas.create_line(self.x, self.y, event.x, event.y, width=2,
                                fill="red", capstyle=ROUND, smooth=True)

        cv2.line(self.master.processed_image, (int(self.x * self.ratio), int(self.y * self.ratio)),
                 (int(event.x * self.ratio), int(event.y * self.ratio)),
                 (0, 0, 255), thickness=int(self.ratio * 2),
                 lineType=8)

        self.x = event.x
        self.y = event.y

    def start_crop(self, event):
        self.master.image_cache.append(self.master.processed_image.copy())
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y,
                                                         self.crop_end_x, self.crop_end_y, width=1)

    def end_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)

        self.master.processed_image = self.master.processed_image[y, x]
        self.master.image_cache.append(self.master.processed_image.copy())

        self.show_image()

    def clear_canvas(self):
        self.canvas.delete("all")

    def undo_image(self):
        if self.master.image_cache:
            self.master.processed_image = self.master.image_cache.pop()
            self.forward_cache.append(self.master.processed_image)
        self.show_image()

    def forward_image(self):
        if self.forward_cache:
            self.master.processed_image = self.forward_cache.pop()
            self.master.image_cache.append(self.master.processed_image)
        self.show_image()
