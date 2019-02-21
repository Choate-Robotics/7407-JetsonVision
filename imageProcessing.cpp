#include <opencv2/opencv.hpp>
#include <vector>
#include <chrono>
#include <stdio.h>
#include <iostream>

//cv::UMat processImage(const cv::UMat &img){
//    //cv::Mat new_img;
//    cv::resize(img,img,cv::Size(480,320));
//
//    cv::GaussianBlur(img,img,cv::Size(3,3),0);
//    cv::cvtColor(img,img,cv::COLOR_RGB2GRAY);
//    cv::threshold(img,img,245,255,cv::THRESH_BINARY);
//    std::vector<std::vector<cv::Point> > contours;
//
//    cv::findContours(img,contours,cv::RETR_EXTERNAL,cv::CHAIN_APPROX_SIMPLE);
//    cv::drawContours(img,contours,-1,cv::Scalar(0,0,255));
//
//    return img;
//}

class VideoStream{
protected:
    cv::Mat frame;
    cv::Size resolution;
    void captureFrame(){
        this->caps>>frame;
    };
    virtual void processFrame(){
        cv::resize(frame,frame,resolution);

    }
public:
    cv::VideoCapture caps;
    VideoStream(int i,int rx, int ry){
        this->resolution=cv::Size(rx,ry);
        this->caps=cv::VideoCapture(i);
    };

    cv::Mat getFrame(){
        captureFrame();
        processFrame();
        return this->frame;
    }
};

class AngleDetection: public VideoStream{
    double angle=0;
    void processFrame() override {
        cv::Mat tmp;
        cv::resize(frame,frame,resolution);
        cv::GaussianBlur(frame,tmp,cv::Size(5,5),0);
        cv::cvtColor(tmp,tmp,cv::COLOR_RGB2GRAY);
        cv::threshold(tmp,tmp,230,255,cv::THRESH_BINARY);

        std::vector<std::vector<cv::Point> > contours;
        cv::findContours(tmp,contours,cv::RETR_TREE,cv::CHAIN_APPROX_SIMPLE);

        int i=0,maxIndex=0;
        double maxArea=-1;

        for (auto &cnt:contours){
            auto area=cv::contourArea(cnt);
            if (area>maxArea){
                maxArea=area;
                maxIndex=i;
            }
            i++;
        }

        cv::drawContours(this->frame,contours,-1,cv::Scalar(0,0,0),1);

        auto rect=cv::minAreaRect(contours[maxIndex]);

        if (rect.size.width>rect.size.height)
            this->angle=-(rect.angle+90);
        else
            this->angle=-rect.angle;



        cv::Point2f vertices[4];
        rect.points(vertices);

        for (int i=0;i<4;i++)
            cv::line(this->frame,vertices[i],vertices[(i+1)%4],cv::Scalar(0,0,255),1,cv::LINE_AA);

        char text[8];
        std::sprintf(text,"%02f",angle);

        cv::putText(frame,text,cv::Point(resolution.width-60,resolution.height-10),cv::FONT_HERSHEY_SIMPLEX,0.5,cv::Scalar(0,0,255));
//    cv::drawContours(img,std::vector<std::vector<cv::Point> >{box},0,cv::Scalar(0,0,255),2);

    }
public:
    AngleDetection(int i, int rx, int ry):VideoStream(i,rx,ry){}
    double getAngle(){
        return angle;
    }
};


int main() {


    auto v=AngleDetection(0,720,480);
    for (;;) {
        auto start= std::chrono::high_resolution_clock::now();
        auto img=v.getFrame();
        //img = processImage(img);
        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
        std::printf("\rTime: %f ms", duration.count() / 1000.0);

        cv::imshow("", img);
        cv::waitKey(1);
    }
}