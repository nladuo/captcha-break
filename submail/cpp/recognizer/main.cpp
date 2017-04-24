#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <map>
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

void load_dataset(vector<Mat> &mats, vector<string> &labels)
{

    fs::path captchas_path("./dataset/");
    std::vector<std::string> images;

    fs::directory_iterator end_iter;
    for (fs::directory_iterator iter(captchas_path); iter != end_iter; ++iter)
    {
        if (fs::extension(*iter)==".png")
        {
            images.push_back(iter->path().string());    //get the filename
            labels.push_back(fs::basename(*iter));
        }
    }

    std::vector<std::string>::iterator itr = images.begin();
    for (;itr != images.end(); ++itr)
    {
        Mat mat = imread(*itr, CV_LOAD_IMAGE_GRAYSCALE);
        mats.push_back(mat);
    }
}


int count_distance(Mat mat1, Mat mat2)
{
    assert(mat1.size().height == mat2.size().height);
    assert(mat1.size().width == mat2.size().width);
    assert(mat1.channels() == 1 && mat2.channels() == 1);

    int distance = 0;

    for(int i = 0; i < mat1.size().width; i++){
        for(int j = 0; j < mat1.size().height; j++){
            if(mat1.at<uchar>(j, i) != mat2.at<uchar>(j, i)){
                distance++;
            }
        }
    }
    return distance;
}


string recognize(Mat mat, vector<Mat> &mats, vector<string> &labels)
{
//    cout<<mats.size()<<endl;
    cv::imshow("2", mat);
    for(int i = 0; i < mats.size(); i++){
//        cout<<labels[i]<<endl;
//        cout<<"size1:"<<mat.size()<<endl;
//        cout<<"size2:"<<mats[i].size()<<endl;
//        cv::imshow("1", mats[i]);
//        waitKey(0);
        if( (mat.size().height == mats[i].size().height)
                && (mat.size().width == mats[i].size().width)
                && (count_distance(mat, mats[i]) == 0) ){

//            cout<<"distance:"<<count_distance(mat, mats[i])<<endl<<endl;
            return labels[i];
        }
    }
    return "UNKNOWN";
}

int main(int argc, char* argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: ./recognizer <image_filename>\n");
        return 1;
    }
    vector<Mat> mats;
    vector<string> labels;
    load_dataset(mats, labels);

    Mat image = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
    Mat image2 = imread(argv[1], CV_LOAD_IMAGE_GRAYSCALE);
    threshold(image, image, 100, 255, cv::THRESH_BINARY);
    threshold(image2, image2, 100, 255, cv::THRESH_BINARY);
    reverse_color(image);
    vector<vector<Point>> contours;
    findContours(image,
                 contours,
                 CV_RETR_EXTERNAL,
                 CV_CHAIN_APPROX_NONE);

    if (contours.size() != 4)
    {
        cout<<"ERROR";return 0;
    }

    map<int, string> result_map;
    vector<int> positions;
    for( int i = 0; i < contours.size(); i++)
    {
        Rect rect = boundingRect(contours[i]);
        Rect rect2;
        rect2.x = rect.x - 2;
        rect2.y = rect.y - 2;
        rect2.width = rect.width + 4;
        rect2.height = rect.height + 4;
        rectangle(image2, rect2, Scalar(255), 1);
        positions.push_back(rect2.x);
        result_map[rect2.x] = recognize(image2(rect2), mats, labels);
        if (result_map[rect2.x] == "UNKNOWN")
        {
            cout<<"ERROR";return 0;
        }
    }

    sort(positions.begin(), positions.end());
    for(int i = 0; i < positions.size(); i++){
        cout<<result_map[positions[i]];
    }

    return 0;
}
