#ifndef OCRDECODER_H
#define OCRDECODER_H
#include <tesseract/baseapi.h>
#include <tesseract/strngs.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <string.h>

class OCRDecoder
{
public:
    void decodeGrayMat(cv::Mat mat, char* result);
};

#endif // OCRDECODER_H
