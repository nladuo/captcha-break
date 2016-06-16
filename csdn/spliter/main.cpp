#include <iostream>
#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/lexical_cast.hpp>
using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: ./spliter <image_filename>\n");
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
        boost::uuids::random_generator rgen;
        boost::uuids::uuid ranUUID = rgen();
        string filename = "./letters/" + boost::lexical_cast<string>(ranUUID) + ".png";
        imwrite(filename, letter);
    }

    return 0;
}
