#ifndef SPLITER_H
#define SPLITER_H
#include "captcha_utils.h"
#include <cmath>
#include <iostream>
#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/lexical_cast.hpp>


class Spliter
{
public:
    Spliter();
    Spliter(std::string save_dir);
    void split_letters(std::string filename, cv::Mat letters[4]);
    void split_and_save(std::string filename);

private:
    CaptchaUtils captcha_utils;
    std::string save_dir;
    void clean_noise(cv::Mat &image);
    void save_image(cv::Mat &splited_mat);

};

#endif // SPLITER_H
