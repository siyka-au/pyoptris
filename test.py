import pyoptris
import cv2

pyoptris.tcp_init('localhost', 1337)

while(True):
    frame = pyoptris.get_palette_image()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pyoptris.terminate()
cv2.destroyAllWindows()