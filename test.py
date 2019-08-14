import numpy as np
import pyoptris as p
from matplotlib import pyplot as plt
import cv2

p.tcp_init('localhost', 1337)

while(True):
    frame = p.get_palette_image()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

p.terminate()
cv2.destroyAllWindows()