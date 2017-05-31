"""
from PIL import ImageGrab
import numpy as np
import cv2

img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
img_np = np.array(img) #this is the array obtained from conversion
frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
cv2.imshow("test", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
import numpy as np
import cv2
from mss import mss
from PIL import Image

#mon = {'top': 160, 'left': 160, 'width': 200, 'height': 200}
mon = {'top': 715, 'left': 50, 'width': 150, 'height': 46}

sct = mss()

while 1:
    #print 'test'
    sct.get_pixels(mon)
    print sct
    img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
    cv2.imshow('test', np.array(img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
