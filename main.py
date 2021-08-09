"""
PixelDorpLaser

Description: We are going to turn a beautiful colorful image into grayscale.
then we are going to colorize it into 8 colors that will be defined by different
laser scanning profile when we print on the laser printer.   What will happen??? I
guess we will find out soon.

Author: Morgan Massens
Date: 2021/08/08

"""


import PIL
from PIL import Image, ImageOps
import requests

from io import BytesIO
from PIL import ImageFilter
from PIL import ImageEnhance
# from IPython.display import display
from math import floor

import os

import numpy as np


colors = {
    0: 'black',
    1: 'red',
    2: 'green',
    3: 'yellow',
    4: 'blue',
    5: 'magenta',
    6: 'cyan',
    7: 'orange'
}

c_list = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 102, 0)
]


class LaserImage:

    def __init__(self):
        # Original imported image
        self.image = None
        self.image_file = ""
        self.image_ext = ""

        # Image turned to grayscale
        self.image_gray = None

        # Image converted back to rgb from grayscale to process
        self.image_laser = None
        self.image_laser_path = ""

    def get_image(self, location):
        if os.path.exists(location):
            self.get_image_from_path(location)

        # TODO Determine if we have an image or not
        return True

    def get_image_from_path(self, path):
        """
        Get the image from a local source
        :param path:
        :return: Image
        """
        try:
            self.image = Image.open(path)
            #self.image.show()
            self.image_file, self.image_ext = os.path.splitext(path)
            return True
        except FileExistsError or PIL.UnidentifiedImageError or ValueError or TypeError:
            return False

    def get_image_from_url(self, url):
        """
        Get the image from a url
        :param url:
        :return: Image
        """
        return

    def convert_to_grayscale(self, threshold=False):
        """
        Convert current loaded image to grayscale as image_gray
        :param threshold:
        :return:
        """
        # Convert image to grayscale and save as self.image_gray
        if self.image:
            self.image_gray = ImageOps.grayscale(self.image)
            #self.image_gray.show()
            return True
        return False

    def convert_to_laser_color(self, threshold=False):
        """
        Convert grayscale image to color levels for defining intensity
        :param threshold:
        :return:
        """

        if self.image_gray:

            # Make the new Laser image
            self.image_laser = Image.new("RGB", self.image_gray.size)

            # Paste the gray image data
            self.image_laser.paste(self.image_gray)

            # Show for good measure
            #self.image_laser.show()

            # Get image dimensions
            image_x, image_y = self.image_laser.size

            self.image_laser.convert(mode='P', colors=8, dither=1)

            pix = self.image_laser.load()

            # Iterate Pixels - divide intensities by (color_val/floor(colors_bits/number_colors))
            for y in range(image_y):
                for x in range(image_x):

                    # Get current Pixel Data
                    r = pix[x, y][0]

                    # Determine and lookup New Color

                    new_pixel_color = c_list[floor(r / 32)]

                    if r > 240:
                        new_pixel_color = (255, 255, 255)

                    # Write the new pixel data
                    pix[x, y] = new_pixel_color

            # Write the new image to a file
            self.image_laser_path = self.image_file + "_new.jpg"
            print(self.image_laser_path)
            self.image_laser.save(self.image_laser_path, "JPEG")

    def convert_to_layers(self):
        """
        Convert the laser image to 8 different color layers
        :return:
        """


if __name__ == '__main__':

    dorp = LaserImage()

    dorp.get_image_from_path(os.path.join('d:', 'share', 'LaserCutting', 'bikini.jpg'))

    dorp.convert_to_grayscale()

    dorp.convert_to_laser_color()

    pass
