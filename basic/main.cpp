#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include "ocr_decoder.h"

using namespace cv;
using namespace std;

int main(int argc, char* argv[])
{
	if(argc != 2) {
        fprintf(stderr, "Usage: ./recognizer <image_filename>\n");
        return 1;
    }
    Mat mat = imread(argv[1], 0);
    Mat threshold_mat;
    cv::threshold(mat, threshold_mat, 150, 255, cv::THRESH_BINARY);

    char buffer[255];
    OCRDecoder decoder;
    decoder.decodeGrayMat(threshold_mat, buffer);
    cout<<"result:"<<buffer<<endl;
}
