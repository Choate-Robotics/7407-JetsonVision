# 7407 Vision Code

This repository contains code that runs on our team's vision co-processor, Nvidia Jetson Tx2. It processes video feed collected from the on-board camera and sends it to our [Dashboard](https://github.com/Choate-Robotics/7407-Dashboard) via UDP sockets. It uses Python primarily, with the image processing written in C++ for performance. 

# Build

The code needs some compilation to work. 
```sh
cd video_frame
cmake .
make
```

# Dependencies

- Python 3.7
- OpenCV 3.4.5
- Boost.Python
- Numpy

