#include <iostream>
#include <string>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/filesystem.hpp>
using namespace std;
using namespace cv;
namespace fs = boost::filesystem;

int main(int argc, char* argv[])
{
    fs::path captchas_path("../downloader/captchas/");
    std::vector<std::string> images;

    //get all captcha files
    fs::directory_iterator end_iter;
    for (fs::directory_iterator iter(captchas_path); iter != end_iter; ++iter)
    {
        if (fs::extension(*iter)==".png") 
        {
            images.push_back(iter->path().string());    //get the filename
        }
    }

    //split all captchas
    std::vector<std::string>::iterator itr = images.begin();
    for (;itr != images.end(); ++itr)
    {
        std::cout<<*itr<<std::endl;
        Mat image = imread(*itr, CV_LOAD_IMAGE_GRAYSCALE);
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
        };
    }

    return 0;
}
