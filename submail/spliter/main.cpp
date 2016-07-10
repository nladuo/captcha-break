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

void reverse_color(cv::Mat& image)
{
    for(int i = 0; i < image.size().width; i++){
        for(int j = 0; j < image.size().height; j++){
            image.at<uchar>(j, i) = 255 - image.at<uchar>(j, i);
        }
    }
}

int main()
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
        try{
            std::cout<<*itr<<std::endl;
            Mat image = imread(*itr, CV_LOAD_IMAGE_GRAYSCALE);
            Mat image2 = imread(*itr, CV_LOAD_IMAGE_GRAYSCALE);
            threshold(image, image, 100, 255, cv::THRESH_BINARY);
            threshold(image2, image2, 100, 255, cv::THRESH_BINARY);
            reverse_color(image);
            vector<vector<Point>> contours;
            findContours(image,
                         contours,
                         CV_RETR_EXTERNAL,
                         CV_CHAIN_APPROX_NONE);

            for( int i = 0; i < contours.size(); i++)
            {
                Rect rect = boundingRect(contours[i]);
                Rect rect2;
                rect2.x = rect.x - 2;
                rect2.y = rect.y - 2;
                rect2.width = rect.width + 4;
                rect2.height = rect.height + 4;
                rectangle(image2, rect2, Scalar(255), 1);
                boost::uuids::random_generator rgen;
                boost::uuids::uuid ranUUID = rgen();
                string filename = "./letters/" + boost::lexical_cast<string>(ranUUID) + ".png";
                imwrite(filename, image2(rect2));
            }

        }catch (Exception ex){
            cout<<ex.msg<<endl;
        }
//        imshow("rect", image2);
    }

    return 0;
}
