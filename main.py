import numpy as np

from projector import Projector
from camera import Camera


p = Projector(np.array([0, 0]), 100, 100, 8)
p.GenerateImage()
