#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    if(argc != 6) {
        fprintf(stderr, "Usage: ./spliter <image_filename> <output_filenames>[4]\n");
        return 1;
    }
    Mat image = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
    threshold(image, image, 100, 255, cv::THRESH_BINARY);
    Range col_ranges[4] = {
        Range(5, 5+8),
        Range(14, 14+8),
        Range(23, 23+8),
        Range(32, 32+8)
    };
    for(int i = 0; i < 4; i++){
        Mat letter = image.colRange(col_ranges[i]);
        string filename(argv[2 + i]);
        filename = "./letters/" + filename + ".png";
        imwrite(filename, letter);
    }

    return 0;
}
