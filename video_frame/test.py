from __init__ import VideoStream, AngleDetection
from PIL import Image
import numpy as np
import time,io

v=VideoStream(0)
print(v)

for i in range(1000):
    start=time.time()
    s=v.getCompressedFrame()
    print((time.time()-start)*1000,'ms')
