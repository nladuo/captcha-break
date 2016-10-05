#ifndef CAPTCHAUTILS_H
#define CAPTCHAUTILS_H
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class CaptchaUtils
{
public:
    CaptchaUtils();
    void clear_noise_line (cv::Mat &image);
    void clear_peper_noise (cv::Mat &image, int max_adhesion_count);

};

#endif // CAPTCHAUTILS_H
