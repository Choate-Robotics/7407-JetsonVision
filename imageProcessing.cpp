#include <opencv2/opencv.hpp>
#include <vector>
#include <chrono>
#include <stdio.h>
#include <iostream>

cv::UMat processImage(const cv::UMat &img){
    //cv::Mat new_img;
    cv::resize(img,img,cv::Size(480,320));

    cv::GaussianBlur(img,img,cv::Size(3,3),0);
    cv::cvtColor(img,img,cv::COLOR_RGB2GRAY);
    cv::threshold(img,img,240,255,cv::THRESH_BINARY);
    std::vector<std::vector<cv::Point> > contours;
    //std::vector<cv::Vec4i> hierarchy;
    cv::findContours(img,contours,cv::RETR_EXTERNAL,cv::CHAIN_APPROX_SIMPLE);
    cv::drawContours(img,contours,-1,cv::Scalar(0,0,255));
    return img;
}

cv::Mat processImage(cv::Mat &img){
    cv::Mat new_img;
    cv::resize(img,img,cv::Size(480,320));

    cv::GaussianBlur(img,new_img,cv::Size(3,3),0);
    cv::cvtColor(new_img,new_img,cv::COLOR_RGB2GRAY);
    cv::threshold(new_img,new_img,240,255,cv::THRESH_BINARY);
    std::vector<std::vector<cv::Point> > contours;
    //std::vector<cv::Vec4i> hierarchy;
    cv::findContours(new_img,contours,cv::RETR_EXTERNAL,cv::CHAIN_APPROX_SIMPLE);
    cv::drawContours(img,contours,-1,cv::Scalar(0,0,255));
    //cv::resize(img,img,cv::Size(1920,1080),cv::INTER_LANCZOS4);
    return img;
}

int main() {

    cv::Mat img = cv::imread("test1.JPG");

    //cv::UMat m=img.getUMat(cv::ACCESS_READ);
    auto start= std::chrono::high_resolution_clock::now();
    img=processImage(img);
    auto stop= std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
    std::printf("Time: %f ms",duration.count()/1000.0);

    cv::imshow("",img);
    cv::waitKey(0);
}