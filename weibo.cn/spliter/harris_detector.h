#ifndef HARRISDETECTOR_H
#define HARRISDETECTOR_H
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class HarrisDetector
{
private:
    cv::Mat cornerStrength;
public:
    HarrisDetector();
};

#endif // HARRISDETECTOR_H
