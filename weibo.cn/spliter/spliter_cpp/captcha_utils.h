#ifndef COMMONUTILS_H
#define COMMONUTILS_H

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>


class CaptchaUtils
{
public:
    CaptchaUtils();
    void clear_peper_noise (cv::Mat &image, int max_adhesion_count);
    void vertical_project(cv::Mat &image, int splits[]);
};

#endif // COMMONUTILS_H
