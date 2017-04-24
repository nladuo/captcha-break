#include "histogram1d.h"

Histogram1D::Histogram1D()
{
    histSize[0] = 256;
    hranges[0] = 0.0;
    hranges[1] = 255.0;
    ranges[0] = hranges;
    channels[0] = 0;
}

cv::MatND Histogram1D::getHistogram (const cv::Mat &image)
{
    cv::MatND hist;
    cv::calcHist (&image, 1, channels, cv::Mat(),hist, 1, histSize, ranges);
    return hist;
}

cv::Mat Histogram1D::getHistogramImage (const cv::Mat &image)
{
    cv::MatND hist = getHistogram (image);
    double maxVal = 0;
    double minVal = 0;
    cv::minMaxLoc (hist, &minVal, &maxVal, 0, 0);

    cv::Mat histImag(histSize[0], histSize[0], CV_8U, cv::Scalar(255));

    int hpt = static_cast<int>(0.9 * histSize[0]);

    for(int h = 0; h < histSize[0]; h++){
        float binVal = hist.at<float>(h);
        int intensity = static_cast<int>(binVal * hpt / maxVal);

        cv::line (histImag, cv::Point(h, histSize[0]),
                cv::Point(h, histSize[0] - intensity),
                cv::Scalar::all (0));
    }
    return histImag;
}
