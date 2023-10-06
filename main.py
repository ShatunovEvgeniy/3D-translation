import numpy as np

from projector import Projector
from camera import Camera


p = Projector(np.array([10, 0, 10]), 70, np.array([16, 16]), 0.6)
p.SetTestProjection(0.001, 0.2)
p.GenerateImage()
p.GenerateImage()
p.GetPlaneEquation(2)
