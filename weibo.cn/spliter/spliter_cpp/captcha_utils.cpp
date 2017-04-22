#include "captcha_utils.h"
#include <vector>
#include <iostream>

CaptchaUtils::CaptchaUtils()
{

}

bool has_tranversed_the_point(int x, int y, std::vector<cv::Point>& tranversed_points)
{
    for(int i = 0; i < tranversed_points.size(); i++){
        if(x == tranversed_points[i].x
                && y == tranversed_points[i].y){
            return true;
        }
    }
    return false;
}

void find_connection_area(cv::Point now_point, cv::Mat image, std::vector<cv::Point>& area,
                          std::vector<cv::Point>& tranversed_points)
{
    using namespace std;
    //return when the point color is white
    if(image.at<uchar>(now_point.y, now_point.x) != 0) return;
    //return when the point is excceed boundary
    if(now_point.x < 0 || now_point.x >= image.size().width
       || now_point.y < 0 || now_point.y >= image.size().height ){
        return;
    }
    //has tranversed
    if(has_tranversed_the_point(now_point.x, now_point.y, tranversed_points)) return;

    //put the tranversed point to vector
    area.push_back(now_point);
    tranversed_points.push_back(now_point);
    // cout<<now_point.x<<"  "<<now_point.y<<endl;

    //recursively find connection area
    find_connection_area(cv::Point(now_point.x, now_point.y-1), image, area, tranversed_points);//上
    find_connection_area(cv::Point(now_point.x, now_point.y+1), image, area, tranversed_points);//下
    find_connection_area(cv::Point(now_point.x-1, now_point.y), image, area, tranversed_points);//左
    find_connection_area(cv::Point(now_point.x+1, now_point.y), image, area, tranversed_points);//右
    find_connection_area(cv::Point(now_point.x-1, now_point.y-1), image, area, tranversed_points);//左上
    find_connection_area(cv::Point(now_point.x-1, now_point.y+1), image, area, tranversed_points);//左下
    find_connection_area(cv::Point(now_point.x+1, now_point.y-1), image, area, tranversed_points);//右上
    find_connection_area(cv::Point(now_point.x+1, now_point.y+1), image, area, tranversed_points);//右下
}


void CaptchaUtils::clear_peper_noise (cv::Mat &image, int max_adhesion_count)
{
    //find connected area
    using namespace std;
    using namespace cv;
    vector<vector<Point> > areas;
    vector<Point> tranversed_points;
    for(int i = 0; i < image.size().width; i++){
        for(int j = 0; j < image.size().height; j++){
            if(image.at<uchar>(j, i) == 0
                    && !has_tranversed_the_point(i, j, tranversed_points)){
                vector<Point> area;
                find_connection_area(cv::Point(i, j), image, area, tranversed_points);

                areas.push_back(area);
            }
        }
    }
    //clean the noises
    for(int i = 0; i < areas.size(); i++){
        if(areas[i].size() <= max_adhesion_count){
            for(int j = 0; j < areas[i].size();j++){
                image.at<uchar>(areas[i][j].y, areas[i][j].x) = 255;
            }
        }
    }

}


void CaptchaUtils::vertical_project (cv::Mat &image, int splits[])
{
    int *project = new int[image.size().width];
    for(int i = 0; i < image.size().width; i++){
        int count = 0;
        for(int j = 1; j < image.size().height - 1; j++){
            if(image.at<uchar>(j, i) == 0){
                count++;
            }
        }
        project[i] = count;
        // std::cout<<i<<" : "<<count<<std::endl;
    }
    int index = 0;
    int i = 1;
    int threshold = 1;
    while(index < 8 && i < 100){
        if((project[i] > threshold && project[i-1] <= threshold)
                || (project[i] <= threshold && project[i-1] > threshold) ){
            if(index % 2 == 1
                    && (i - splits[index-1]) <= 8 ) {
                i++;
                continue;
            }
            splits[index] = i;
            index ++;
        }
        i++;
    }
    delete[] project;
}


