/*
    Copyright (c) 2013, Taiga Nomi
    All rights reserved.
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
    names of its contributors may be used to endorse or promote products
    derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND 
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "tiny_cnn/tiny_cnn.h"
#include "spliter.h"

using namespace tiny_cnn;
using namespace tiny_cnn::activation;
using namespace std;

std::string label_strs[14] = {
    "3", "C", "D", "E", "F", "H", "J", "K", "L", "M", "N", "W", "X", "Y"
};

// rescale output to 0-100
template <typename Activation>
double rescale(double x) {
    Activation a;
    return 100.0 * (x - a.scale().first) / (a.scale().second - a.scale().first);
}

void convert_mat(cv::Mat &img,
    double minv,
    double maxv,
    int w,
    int h,
    vec_t& data) {
    if (img.data == nullptr) return; // cannot open, or it's not an image

    cv::Mat_<uint8_t> resized;
    cv::resize(img, resized, cv::Size(w, h));

    // mnist dataset is "white on black", so negate required
    std::transform(resized.begin(), resized.end(), std::back_inserter(data),
        [=](uint8_t c) { return (255 - c) * (maxv - minv) / 255.0 + minv; });
}


void construct_net(network<sequential>& nn) {
    // connection table [Y.Lecun, 1998 Table.1]
#define O true
#define X false
    static const bool tbl[] = {
        O, X, X, X, O, O, O, X, X, O, O, O, O, X, O, O,
        O, O, X, X, X, O, O, O, X, X, O, O, O, O, X, O,
        O, O, O, X, X, X, O, O, O, X, X, O, X, O, O, O,
        X, O, O, O, X, X, O, O, O, O, X, X, O, X, O, O,
        X, X, O, O, O, X, X, O, O, O, O, X, O, O, X, O,
        X, X, X, O, O, O, X, X, O, O, O, O, X, O, O, O
    };
#undef O
#undef X

    // construct nets
    nn << convolutional_layer<tan_h>(32, 32, 5, 1, 6)  // C1, 1@32x32-in, 6@28x28-out
       << average_pooling_layer<tan_h>(28, 28, 6, 2)   // S2, 6@28x28-in, 6@14x14-out
       << convolutional_layer<tan_h>(14, 14, 5, 6, 16,
            connection_table(tbl, 6, 16))              // C3, 6@14x14-in, 16@10x10-in
       << average_pooling_layer<tan_h>(10, 10, 16, 2)  // S4, 16@10x10-in, 16@5x5-out
       << convolutional_layer<tan_h>(5, 5, 5, 16, 120) // C5, 16@5x5-in, 120@1x1-out
       << fully_connected_layer<tan_h>(120, 14);       // F6, 120-in, 14-out
}

int recognize(const std::string& dictionary, cv::Mat &img) {
    network<sequential> nn;

    construct_net(nn);

    // load nets
    ifstream ifs(dictionary.c_str());
    ifs >> nn;

    // convert cvMat to vec_t
    vec_t data;
    convert_mat(img, -1.0, 1.0, 32, 32, data);

    // recognize
    auto res = nn.predict(data);
    vector<pair<double, int> > scores;

    for (int i = 0; i < 14; i++)
        scores.emplace_back(rescale<tan_h>(res[i]), i);

    // sort and get the result
    sort(scores.begin(), scores.end(), greater<pair<double, int>>());
    return scores[0].second;
}

cv::Mat resize_mat(cv::Mat &splited_mat)
{
    //put the mat in center of 32*32 pixels image.
    int out_height = 32;
    int out_width = 32;
    cv::Mat out(out_height, out_width, CV_8UC1,cv::Scalar(255));
    int offset_x = (out_width - splited_mat.size().width)/2;
    int offset_y = (out_height - 20)/2;
    cv::Mat imageROI;
    imageROI = out(cv::Rect(offset_x, offset_y, splited_mat.cols, splited_mat.rows));
    splited_mat.copyTo(imageROI);

    return out;
}


int main(int argc, char** argv) {
    if (argc != 2) {
        cout << "please specify image file";
        return 0;
    }
    Spliter spliter("");
    cv::Mat letters[4];
    spliter.split_letters(argv[1], letters);
    cout<<"Result:";
    for(int i = 0; i < 4; i++){
        cv::Mat r_mat = resize_mat(letters[i]);
        int res = recognize("weibo.cn-nn-weights", r_mat);
        cout<<label_strs[res];
    }
    cout<<endl;

}
