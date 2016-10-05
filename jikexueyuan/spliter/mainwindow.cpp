#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QFileDialog>
#include <QMessageBox>

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

int getSamplesNum(cv::Mat &image)
{
    int samples_num = 0;
    for( int i = 0; i < image.size().width; i++ ){
        for( int j = 0; j < image.size().height; j++ ) {
            if(image.at<uchar>(j, i) == 0){
                samples_num++;
            }
        }
    }
    return samples_num;
}

cv::Mat createSamples(cv::Mat &image, int samples_num)
{
    cv::Mat samples(samples_num, 2, CV_32FC1);
    int index = 0;
    for( int i = 0; i < image.size().width; i++ ){
        for( int j = 0; j < image.size().height; j++ ) {
            if(image.at<uchar>(j, i) == 0){
                samples.at<float>(index, 0) = i;
                samples.at<float>(index, 1) = j;
                index++;
            }
        }
    }
    return samples;
}

void startEM(std::string src)
{
    cv::Mat image_colored =  cv::imread(src, 1);
    cv::Mat image = cv::imread(src, 0);
    cv::threshold(image, image, 100, 255, cv::THRESH_BINARY);
    cv::imshow("threshold", image);
    CaptchaUtils utils;
    utils.clear_noise_line(image);
    utils.clear_peper_noise(image, 10);


    cv::EM em(4, cv::EM::COV_MAT_SPHERICAL ); //4 clusters
    int samples_num = getSamplesNum(image);
    cv::Mat samples = createSamples(image, samples_num);

    if (!em.train(samples)) {
        std::cerr << "error training the EM model" << std::endl;
        exit(-1);
    }

    const cv::Mat& means = em.get<cv::Mat>("means");
    cv::imshow("means", means);
    std::cout<<means.cols<<" "<<means.rows<<std::endl;

    cv::Mat sample_predict = cv::Mat( 2, 1, CV_32FC1 );
    cv::Vec3b colors[4] = {
        cv::Vec3b(111, 0, 111),
        cv::Vec3b(0, 111, 111),
        cv::Vec3b(111, 111, 0),
        cv::Vec3b(111, 0, 0),
    };
    for( int i = 0; i < image.size().width; i++ ){
        for( int j = 0; j < image.size().height; j++ ) {
            sample_predict.at<float>(0) = (float)i;
            sample_predict.at<float>(1) = (float)j;
            cv::Vec2d value = em.predict( sample_predict );
            int type = value[1];
            if(image.at<uchar>(j, i) == 255){
                image_colored.at<cv::Vec3b>(j, i) = colors[type];
            }
        }
    }
    cv::imshow("image", image);
    cv::imshow("colored", image_colored);
}

void MainWindow::on_pushButton_clicked()
{
    QString openPath = "/home/kalen/captchas";
    QString path = QFileDialog::getOpenFileName(this, tr("Open Image"), openPath, tr("Image Files(*.jpg *.png)"));
    if(path.length() == 0) {
        QMessageBox::information(NULL, tr("Path"), tr("You didn't select any files."));
    } else {
        startEM(path.toStdString());
    }
}

