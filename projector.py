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

    def StripeArray(self) -> np.array:
        """
        Create a np.array() of stripes order for each iteration

        :return: np.array() with shape=(log2(count), count - 1)
        where a line number is number of a stripe projection and a column number is number of each stipe.
        So (i, j) element shows if in an i-iteration a j-stripe is shown or not
        """
        image_count = log2(self.stripe_count)  # count of projection needing for 2D->3D translation
        if trunc(image_count) != image_count:
            raise ValueError("Count of stripes in StripeArray(count) has to be a power of 2.")
        image_count = int(image_count)

        image_count_str = '0' + str(image_count + 2) + 'b'
        bins = [format(i, image_count_str)[2:] for i in range(self.stripe_count)]  # array of bin numbers,
        # preparation for result array

        stripe_array = np.zeros((image_count, self.stripe_count), dtype=int)
        # there is stripe_count - 1 because a column of zeros doesn't have sense (means a stripe we never see)

        for i in range(self.stripe_count):
            stripe_array[..., i] = np.array([int(j) for j in bins[i]]).T
        print(stripe_array)
        return stripe_array

    def GenerateImage(self) -> np.array:
        """
        Create an image for current stripe order

        :return: np.array - desired image
        """
        image = np.zeros((self.width, self.height))
        stripes = np.where(self.stripes_order[self.image_index] == 1)[0]  # indexes of stripes which are on
        for stripe in stripes:
            x0 = self.strip_width * stripe  # coordinate of the start of a stripe
            image[:, x0:x0 + self.strip_width] = 1

        self.image_index += 1
        return image

