#include <opencv2/opencv.hpp>


#include <stdio.h>
#include <iostream>

cv::Mat processImage(){
    cv::UMat img = cv::imread("/Users/jerry/Downloads/IMG_0257.JPG").getUMat(cv::ACCESS_READ);
    return img.getMat(cv::ACCESS_READ);

}


int main() {

    cv::Mat img = processImage();


    cv::imshow("",img);
    cv::waitKey(0);
}