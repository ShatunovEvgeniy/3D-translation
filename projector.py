from math import log2, floor
import numpy as np


class Projector:
    def __init__(self, position, angle: float, projector_resolution, accuracy=0.5):
        """
        :param position: np.array([x, y, z]):
                Coordinates in the coordinate system associated with the camera
                where Oy, Ox are directed as usually for images in system of the camera,
                Oz is directed to an object from the camera (right-handed coordinate system).
                The center of a coordinate system is in the camera focus.
        :param angle:[0, 90]: Angle related to the camera.
        :param projector_resolution: np.array([h, w]): Resolution of projector in pixels (etc. 1024x768).
        :param accuracy:[0...1]: Shows how many stripes will be according to resolution in the last image.
        """
        self.position = position
        self.angle = angle

        self.height = projector_resolution[1]  # height of an output stripe image in pixels
        self.width = projector_resolution[0]  # width of an output stipe image in pixels

        self.image_count = self.FindImageCount(accuracy)
        self.stripe_count = 2 ** self.image_count  # count of stripes in the last image

        self.stripes_order = self.StripeArray()  # np.array(log2(count), count-1) with order of stripes in iterations
        self.strip_width = self.width // self.stripe_count
        # the last strip has a calculation error of stripe_width
        self.last_stripe_width = self.strip_width + self.width % self.stripe_count

        self.image_index = 0  # index of last generated image

        ''' It needs to translate pixels in metres to get a plane equation for each stripe. 
            For that reason there is an experiment where an image is projected on a screen 
                which is not far away from the projector.
            It is also possible to use default value.
        '''
        self.pixel_in_meters = 0.000264583333337192  # length of a pixel in metres
        self.test_distance = None  # distance for a screen with a test projection

    def FindImageCount(self, accuracy: float) -> int:
        """
        Find count of images in process.

        :param accuracy:[0...1]: which shows how many images will be according to resolution.
                        If accuracy 1 it will be max possible power of 2.

        :return: Count of images.
        """
        max_count = floor(log2(self.width))
        needed_count = floor(max_count * accuracy)
        return needed_count

    def StripeArray(self) -> np.array:
        """
        Create a np.array() of stripes order for each iteration.

        :return: np.array(), shape=(log2(stripe_count), stripe_count - 1):
                A line number is number of an image and a column number is number of each stipe.
                So (i, j) element shows if in an i-iteration a j-stripe is shown or not
        """

        image_count_str = '0' + str(self.image_count + 2) + 'b'
        bins = [format(i, image_count_str)[2:] for i in range(self.stripe_count)]  # array of bin numbers,
        # preparation for result array

        stripe_array = np.zeros((self.image_count, self.stripe_count), dtype=int)

        for i in range(self.stripe_count):
            stripe_array[..., i] = np.array([int(j) for j in bins[i]]).T
        print(stripe_array)
        return stripe_array

    def SetTestProjection(self, distance: float, width: float) -> None:
        """
        Set measured data in test projection to calculate points of a plane for each stripe
        which are needed in GetPlaneEquation.

        :param distance: Distance in meters from the projector to projection surface.
        :param width:
        :return: None
        """
        self.test_distance = distance
        self.pixel_in_meters = width / self.width

    def GenerateImage(self) -> np.array:
        """
        Create an image for current stripe order

        :return: Desired image
        """
        image = np.zeros((self.width, self.height))
        stripes = np.where(self.stripes_order[self.image_index] == 1)[0]  # indexes of stripes which are on
        for stripe in stripes:
            x0 = self.strip_width * stripe  # coordinate of the start of a stripe
            image[:, x0:x0 + self.strip_width] = 1

        self.image_index += 1
        return image

    def GetPlaneEquation(self, stripe_number: int) -> np.array:
        """
        Create a np.array() with plane parameters a,b,c,d of the stripe.
        To avoid calculation of planes for each pixel of a stripe it calculates only for middle pixel.
        Equation is calculated by 3 points which belong to a plane.

        :param stripe_number: number of a stripe which plate is calculating
        :return: np.array([a, b, c, d])
                 where a, b, c, d are parameters of plane
        """
        width = self.strip_width
        if stripe_number == self.stripe_count - 1:
            width = self.last_stripe_width
