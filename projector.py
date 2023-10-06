from math import log2, trunc
import numpy as np


class Projector:
    def __init__(self, position, height, width, stripe_count):
        self.stripe_count = stripe_count
        self.position = position  # position of the projector relative to the camera
        self.stripes_order = self.StripeArray()  # order of stripes in each iteration
        self.height = height  # height of projection image
        self.width = width  # width of projection image
        self.strip_width = width // stripe_count
        self.image_index = 0  # index of last generated image

