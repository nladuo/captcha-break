#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <QFileDialog>
#include <cmath>
#include <iostream>
#include <string>
#include <QUuid>
#include "histogram1d.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

bool is_black(int i, int j, cv::Mat &image)
{
    int b =  image.at<cv::Vec3b>(j, i)[0];
    int g =  image.at<cv::Vec3b>(j, i)[1];
    int r =  image.at<cv::Vec3b>(j, i)[2];
    int average = (r + g + b)/3;
    if( r <244 &&  (abs(average-b) < 4)
        && (abs(average-g) < 4)
        && (abs(average-r) < 4)){
        return true;
    }
    return false;
}

/**
 * 清除颜色
 * @brief clear_color
 * @param image
 */
void clear_color(cv::Mat& image)
{
    for(int i = 0; i < image.size().width; i++){
        for(int j = 0; j < image.size().height; j++){
           if(is_black(i, j, image)){
               image.at<cv::Vec3b>(j, i)[0] = 20;
               image.at<cv::Vec3b>(j, i)[1] = 20;
               image.at<cv::Vec3b>(j, i)[2] = 20;
           }
        }
    }
}


int get_horizontal_noise_line_width(cv::Mat &image, int now_height, int now_width)
{
    using namespace std;
    int end_width = now_width;
    while(end_width < image.size().width
          && image.at<cv::Vec3b>(now_height, end_width)[0] < 12
          && image.at<cv::Vec3b>(now_height, end_width)[1] < 12
          && image.at<cv::Vec3b>(now_height, end_width)[2] < 12){
//        cout<<
//          int(image.at<cv::Vec3b>(now_height, end_width)[0])<< " "<<
//          int(image.at<cv::Vec3b>(now_height, end_width)[1])<< " "<<
//          int(image.at<cv::Vec3b>(now_height, end_width)[2])<< " "<<endl;
        end_width++;
    }
    return end_width - now_width;
}



void clear_horizontal_noise_line(cv::Mat &image)
{
    using namespace std;
    int first_height;
    bool has_find = false;
    for(int i = 0; i < image.size().height; i++){
        //水平上连续三个点都是很黑的
        if(image.at<cv::Vec3b>(i, 0)[0] < 12
                && image.at<cv::Vec3b>(i, 0)[1] < 12
                && image.at<cv::Vec3b>(i, 0)[2] < 12
                && get_horizontal_noise_line_width(image, i, 0) >= 2 ){
            first_height = i;
            has_find = true;
        }
    }
    //cout<<"first:"<<first_height<<endl;
    int now_width = 0;
    int now_height = first_height;
    while(now_width < image.size().width){
        int width = get_horizontal_noise_line_width(image, now_height, now_width);
        //cout<<now_width<<"  "<<now_height<< " width:"<<width<<endl;
        //清除直线
        for(int i = now_width; i < now_width + width; i++){
            int top_num = 0;
            int bottom_num = 0;
            //上面的点
            if(is_black(i, now_height-1, image)) top_num++;
            //左上面的点
            if(is_black(i-1, now_height-1, image)) top_num++;
            //右上面的点
            if(is_black(i+1, now_height-1, image)) top_num++;
            //下面的点
            if(is_black(i, now_height+1, image)) bottom_num++;
            //左下面的点
            if(is_black(i-1, now_height+1, image)) bottom_num++;
            //右下面的点
            if(is_black(i+1, now_height+1, image)) bottom_num++;

            if(now_height != 0 && now_height != image.size().height){
                if(top_num>0 && bottom_num>0) continue;
            }

            image.at<cv::Vec3b>(now_height, i)[0] = 255;
            image.at<cv::Vec3b>(now_height, i)[1] = 255;
            image.at<cv::Vec3b>(now_height, i)[2] = 255;
        }

        //寻找下一个点的位置
        int a = get_horizontal_noise_line_width(image, now_height - 1, now_width + width -1);
        int b = get_horizontal_noise_line_width(image, now_height + 1, now_width + width -1);
        int c = get_horizontal_noise_line_width(image, now_height - 1, now_width + width);
        int d = get_horizontal_noise_line_width(image, now_height + 1, now_width + width);
        if(now_height == 0) a=0,c=0;
        if(now_height == (image.size().height - 1) ) b=0,d=0;
        //cout<<"abcd: "<<a<<" "<<b<<" "<<c<<" "<<d<<endl;

        int max_a_b =  a>b?a:b;
        int max_c_d =  c>d?c:d;
        int max_a_b_c_d = max_a_b>max_c_d?max_a_b:max_c_d;
        //cout<<"max_abcd:"<<max_a_b_c_d<<endl;
        if(max_a_b_c_d < 2) break;
        if(max_a_b == max_a_b_c_d){//下一个点在正上方或者在正下方
            now_width += width-1;
            if(max_a_b == a){
                now_height -= 1;
            }else{
                now_height += 1;
            }
        }else{//下一个点在斜着的方法
            now_width += width;
            if(max_c_d == c){
                now_height -= 1;
            }else{
                now_height += 1;
            }
        }
    }
}


void reverse_color(cv::Mat& image)
{
    for(int i = 0; i < image.size().width; i++){
        for(int j = 0; j < image.size().height; j++){
            image.at<uchar>(j, i) = 255 - image.at<uchar>(j, i);
        }
    }
}

bool find_white_point(cv::Mat image, cv::Point_<uchar>& point)
{
    //左右边界遍历
    for(int j = 0; j < image.size().height - 1; j++){
        if(image.at<cv::Vec3b>(j, 0)[0] == 255
                && image.at<cv::Vec3b>(j, 0)[1] == 255
                && image.at<cv::Vec3b>(j, 0)[2] == 255){
            point.x = 0;
            point.y = j;
            return true;
        }else if(image.at<cv::Vec3b>(j, image.size().width - 1)[0] == 255
                && image.at<cv::Vec3b>(j, image.size().width - 1)[1] == 255
                && image.at<cv::Vec3b>(j, image.size().width - 1)[2] == 255){
            point.x = image.size().width - 1;
            point.y = j;
            return true;
        }
    }
    //上下边界遍历
    for(int i = 0; i < image.size().width - 1; i++){
        if(image.at<cv::Vec3b>(0, i)[0] == 255
                && image.at<cv::Vec3b>(0, i)[1] == 255
                && image.at<cv::Vec3b>(0, i)[2] == 255){
            point.x = i;
            point.y = 0;
            return true;
        }else if(image.at<cv::Vec3b>(image.size().height - 1, i)[0] == 255
                && image.at<cv::Vec3b>(image.size().height - 1, i)[1] == 255
                && image.at<cv::Vec3b>(image.size().height - 1, i)[2] == 255){
            point.x = i;
            point.y = image.size().height - 1;
            return true;
        }
    }

    for(int i = 1; i < image.size().width - 1; i++){
        for(int j = 1; j < image.size().height - 1; j++){
            if(image.at<cv::Vec3b>(j, i)[0] == 255
                    && image.at<cv::Vec3b>(j, i)[1] == 255
                    && image.at<cv::Vec3b>(j, i)[2] == 255){
                point.x = i;
                point.y = j;
                return true;
            }
        }
    }
    return false;
}

void differential_process(cv::Mat& mat)
{
    cv::Mat clone_mat = mat.clone();
    for(int i = 0; i < mat.size().width - 1; i++){
        for(int j = 0; j < mat.size().height; j++){
            if(clone_mat.at<uchar>(j, i) != clone_mat.at<uchar>(j, i+1)){
                mat.at<uchar>(j, i) = 0;
            }else{
                mat.at<uchar>(j, i) = 255;
            }
        }
    }

}

void save_image(cv::Mat &image)
{

}

void MainWindow::on_pushButton_clicked()
{
    QString filename = QFileDialog::getOpenFileName (this,
                    tr("Open img"), "/home/kalen/Pictures/captchas",
                    tr("Image files (*.png *.jpg *.jpeg *.bmp)"));

    if(filename.size () == 0) return;
    //read the image
    cv::Mat image =  cv::imread (filename.toStdString (), CV_LOAD_IMAGE_COLOR);
    cv::imshow ("init", image);

    //清除干扰线
    cv::flip (image, image, -1);
    clear_horizontal_noise_line(image);
    cv::flip (image, image, -1);
    clear_horizontal_noise_line(image);
    clear_color(image);
    cv::imshow("clear", image);

    //threshold the image
    cv::cvtColor(image, image, CV_BGR2GRAY);//BGR转灰度
    cv::Mat thresholded_img;
    cv::threshold (image, thresholded_img, 150, 255, cv::THRESH_BINARY);
    cv::imshow ("thresholded", thresholded_img);

    //去除椒盐噪声
    captcha_utils.clear_peper_noise(thresholded_img, 2);
    cv::imshow("clear peper:", thresholded_img);


    int splits[8];
    captcha_utils.vertical_project (thresholded_img, splits);
    cv::Mat clone_mat = thresholded_img.clone();
    for(int i = 0; i < 8; i++){
        std::cout<<i<<" "<<splits[i]<<std::endl;
        cv::line (clone_mat, cv::Point(splits[i], 0), cv::Point(splits[i], 20), cv::Scalar(0));
    }
    cv::imshow ("split", clone_mat);
    if(splits[7] < 100){
        for(int i = 0; i < 8; i += 2){
            cv::Rect rect(cv::Point(splits[i], 0), cv::Point(splits[i+1], 20));
            cv::Mat mat = thresholded_img(rect);
            cv::imwrite(QUuid().createUuid().toString().toStdString() + ".png", mat);
        }
    }



    //导出
//    std::string uuid = QUuid::createUuid().toString().toStdString();
//    std::string outFile = "/Users/kalen/" + uuid + ".png";
//    cv::imwrite(outFile, thresholded_img);




//    captcha_utils.clear_single_pixel_line (clear_image);
//
//    captcha_utils.clear_single_pixel_point (clear_image);
//    cv::imshow("clear", clear_image);


//    cv::cvtColor(clear_image, clear_image, CV_GRAY2BGR);//灰度转BGR

//    cv::Point_<uchar> point;
//    cv::Scalar scalars[1 + 5*5*5 - 4];
//    scalars[0] = cv::Scalar(240, 240, 240);
//    int index = 1;
//    for(int i = 1; i < 6; i++){
//        for(int j = 1; j < 6; j++){
//            for(int k = 1; k < 6; k++){
//                if(i == j && j == k && i == k){
//                    continue;
//                }
//                int unit = 155/(5+1);
//                scalars[index++] = cv::Scalar(100 + i*unit, 100 + j*unit, 100 + k*unit);
//            }
//        }
//    }

//    index = 1;
//    while(find_white_point(clear_image, point)){
//        if(point.x == 0 || point.y == 0 || point.x == 99 || point.y == 19){
//            cv::floodFill(clear_image, point, scalars[0]);
//        }else{
//            cv::floodFill(clear_image, point, scalars[index++]);
//        }
//    }
//    cv::imshow("flood", clear_image);



//    cv::cvtColor(resize_image,resize_image, CV_BGR2GRAY);
//    cv::threshold (resize_image, resize_image, 220, 255, cv::THRESH_BINARY);
//    cv::imshow ("resize_and_threshold", resize_image);

//    Histogram1D histogram1D;
//    cv::Mat histogram_image = histogram1D.getHistogramImage(image);
//    cv::imshow("histogram image", histogram_image);








//    cv::floodFill(clear_image, cv::Point(0, 0), cv::Scalar(255));
//    cv::imshow ("flood", clear_image);

////    cv::Mat eroded;
//    cv::erode(resize_image, resize_image, cv::Mat());
//    cv::erode(resize_image, resize_image, cv::Mat());
//    cv::imshow("eroded", resize_image);

//    cv::imshow("clear", clear_image);

//    reverse_color(clear_image);
//    cv::imshow("reverse", clear_image);

//    std::vector<std::vector<cv::Point>> contours;
//    //findContours的输入是二值图像
//    cv::findContours(clear_image,
//            contours, // a vector of contours
//            CV_RETR_EXTERNAL, // retrieve the external contours
//            CV_CHAIN_APPROX_NONE); // retrieve all pixels of each contours
//    std::cout << "Contours: " << contours.size() << std::endl;
//    std::vector<std::vector<cv::Point>>::const_iterator itc_rec= contours.begin();
//    while (itc_rec!=contours.end())
//    {
//        cv::Rect r0= cv::boundingRect(cv::Mat(*(itc_rec)));
//        cv::rectangle(image,r0,cv::Scalar(0),1);
//            ++itc_rec;
//    }
//    cv::imshow("result", image);

//    cv::drawContours(clear_image,contours,
//            -1, // draw all contours
//            cv::Scalar(255),
//            2); // with a thickness of 2
//    cv::imshow("contours", clear_image);





}
