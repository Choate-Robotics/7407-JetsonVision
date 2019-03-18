#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/module.hpp>
#include <boost/python/overloads.hpp>
#include "videoFrame.h"
#include <string>
#include <fstream>

int i=0;
struct vector_to_bytes{
    static PyObject* convert(std::vector<unsigned char> const &vec){
        return PyBytes_FromStringAndSize((char *)&vec[0],vec.size());
    }
};

BOOST_PYTHON_MODULE(video_frame){
    using namespace boost::python;
    to_python_converter<std::vector<unsigned char>,vector_to_bytes>();

    class_<VideoStream>("VideoStream",init<int,int,int,int>())
            .def("getCompressedFrame",&VideoStream::getCompressedFrame)
            .def("setQuality",&VideoStream::setQuality,args("quality"))
            .def("setResolution",&VideoStream::setResolution,args("width"))
            .def("getWidth",&VideoStream::getWidth)
            .def("getHeight",&VideoStream::getHeight)
            .def("getQuality",&VideoStream::getQuality)
            .def("getId",&VideoStream::getId)
            ;

    class_<AngleDetection>("AngleDetection",init<int,int,int,int>())
            .def("getCompressedFrame",&AngleDetection::getCompressedFrame)
            .def("getAngle",&AngleDetection::getAngle)
            .def("setQuality",&AngleDetection::setQuality,args("quality"))
            .def("setResolution",&AngleDetection::setResolution,args("width"))
            .def("getWidth",&AngleDetection::getWidth)
            .def("getHeight",&AngleDetection::getHeight)
            .def("getQuality",&AngleDetection::getQuality)
            .def("getId",&AngleDetection::getId)
            ;


}

