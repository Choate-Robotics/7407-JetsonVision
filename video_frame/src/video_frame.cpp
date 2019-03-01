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


//        std::printf("Converter Called\n");
        const unsigned char * p=&vec[0];
/*
        char filename[16];
        std::sprintf(filename,"img/C%d.jpg",i++);
        std::ofstream out(filename);
        out.write(reinterpret_cast<const char *>(p),vec.size());
        out.close();
        std::printf("%d bytes written to %s ",(int)vec.size(),&filename[0]);
        for (char c:vec){
            std::printf("%x",c);
        }
        std::printf("\n");
*/

        return PyMemoryView_FromMemory((char *)p,vec.size(),PyBUF_READ);
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

