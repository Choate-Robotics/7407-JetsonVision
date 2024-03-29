#include <chrono>
#include <stdio.h>
#include <iostream>

#include "videoFrame.h"


int main() {
    auto v=CannyEdge(0,720,480,100);
    auto last= std::chrono::high_resolution_clock::now();
    for (;;) {

        auto img=v.getFrame();
        //auto buf=v.getCompressedFrame();
       auto now = std::chrono::high_resolution_clock::now();
       auto duration = std::chrono::duration_cast<std::chrono::microseconds>(now - last);
        std::printf("\rTime: %f ms", duration.count() / 1000.0);
      last=now;
      cv::imshow("", img);
      cv::waitKey(1);
    }
}
