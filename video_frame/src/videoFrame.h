#ifndef VIDEOFRAME_VIDEOFRAME_H
#define VIDEOFRAME_VIDEOFRAME_H

#include <opencv2/opencv.hpp>
#include <vector>

class VideoStream {
protected:
    cv::Mat frame;
    cv::Size resolution;
    int quality;
    int id;

    void captureFrame() {
        this->caps >> frame;
    };

    virtual void processFrame() {
        cv::resize(frame, frame, resolution);
    }

public:
    cv::VideoCapture caps;

    VideoStream(int i, int rx, int ry) {
        this->resolution = cv::Size(rx, ry);
        this->caps = cv::VideoCapture(i);
        this->id = i;
        if (!caps.isOpened())
            std::printf("Video capture for cam %d failed", i);
    };

    ~VideoStream() {
        caps.release();
    }

    cv::Mat getFrame() {
        captureFrame();
        processFrame();
        return this->frame;
    }

    std::vector<unsigned char> getCompressedFrame() {
        std::vector<uchar> buf;
        captureFrame();
        processFrame();
        cv::imencode(".jpg", frame, buf, std::vector<int>{
                cv::IMWRITE_JPEG_QUALITY, quality,
                cv::IMWRITE_JPEG_OPTIMIZE, 1,

        });
        return buf;
    }

    void setResolution(int width, int height) {
        this->resolution = cv::Size(width, height);
    }

    int getHeight(){
        return resolution.height;
    }

    int getWidth(){
        return resolution.width;
    }

    void setQuality(int q){
        this->quality=q;
    }

    int getQuality(){
        return quality;
    }

    int getId(){
        return id;
    }

};

class AngleDetection : public VideoStream {
    double angle = 0;

    void processFrame() override {
        cv::Mat tmp;
        cv::resize(frame, frame, resolution);
        cv::GaussianBlur(frame, tmp, cv::Size(5, 5), 0);
        cv::cvtColor(tmp, tmp, cv::COLOR_RGB2GRAY);
        cv::threshold(tmp, tmp, 230, 255, cv::THRESH_BINARY);

        std::vector<std::vector<cv::Point> > contours;
        cv::findContours(tmp, contours, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);

        int i = 0, maxIndex = 0;
        double maxArea = -1;

        for (auto &cnt:contours) {
            auto area = cv::contourArea(cnt);
            if (area > maxArea) {
                maxArea = area;
                maxIndex = i;
            }
            i++;
        }

        cv::drawContours(this->frame, contours, -1, cv::Scalar(0, 0, 0), 1);

        auto rect = cv::minAreaRect(contours[maxIndex]);

        if (rect.size.width > rect.size.height)
            this->angle = -(rect.angle + 90);
        else
            this->angle = -rect.angle;


        cv::Point2f vertices[4];
        rect.points(vertices);

        for (int i = 0; i < 4; i++)
            cv::line(this->frame, vertices[i], vertices[(i + 1) % 4], cv::Scalar(0, 0, 255), 1, cv::LINE_AA);

        char text[8];
        std::sprintf(text, "%02f", angle);

        cv::putText(frame, text, cv::Point(resolution.width - 60, resolution.height - 10), cv::FONT_HERSHEY_SIMPLEX,
                    0.5, cv::Scalar(0, 0, 255));
//    cv::drawContours(img,std::vector<std::vector<cv::Point> >{box},0,cv::Scalar(0,0,255),2);

    }

public:
    AngleDetection(int i, int rx, int ry) : VideoStream(i, rx, ry) {}

    ~AngleDetection() {
        caps.release();
    }

    double getAngle() {
        return angle;
    }
};


#endif //VIDEOFRAME_VIDEOFRAME_H
