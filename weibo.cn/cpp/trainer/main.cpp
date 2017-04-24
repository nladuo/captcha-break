#include <iostream>
#include <boost/filesystem.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "tiny_cnn/tiny_cnn.h"

using namespace tiny_cnn;
using namespace tiny_cnn::activation;
namespace fs = boost::filesystem;

std::string label_strs[14] = {
    "3", "C", "D", "E", "F", "H", "J", "K", "L", "M", "N", "W", "X", "Y"
};

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

// convert image to vec_t
void convert_image(const std::string& imagefilename,
    double minv,
    double maxv,
    int w,
    int h,
    vec_t& data) {
    auto img = cv::imread(imagefilename, cv::IMREAD_GRAYSCALE);
    if (img.data == nullptr) return; // cannot open, or it's not an image

    cv::Mat_<uint8_t> resized;
    cv::resize(img, resized, cv::Size(w, h));

    // mnist dataset is "white on black", so negate required
    std::transform(resized.begin(), resized.end(), std::back_inserter(data),
        [=](uint8_t c) { return (255 - c) * (maxv - minv) / 255.0 + minv; });
}


void load_dataset(std::vector<label_t> &train_labels,
                  std::vector<vec_t> &train_images,
                  std::vector<label_t> &test_labels,
                  std::vector<vec_t> &test_images)
{
    for (int i = 0; i < 14; ++i){
        std::vector<std::string> images;

        fs::directory_iterator end_iter;
        fs::path path("./training_set/"+label_strs[i]);
        for (fs::directory_iterator iter(path); iter != end_iter; ++iter){
            if (fs::extension(*iter)==".png"){
                images.push_back(iter->path().string());
            }
        }

        //train_set.size() : test_set.size() = 4:1
        int flag = 0;
        std::vector<std::string>::iterator itr = images.begin();
        for (;itr != images.end(); ++itr){
            vec_t data;
            convert_image(*itr, -1.0, 1.0, 32, 32, data);
            if (flag <= 4){
                train_labels.push_back(i);
                train_images.push_back(data);
            }else{
                test_labels.push_back(i);
                test_images.push_back(data);
                flag = 0;
            }
            flag++; 
        }
    }
}

int main(int argc, char **argv) {
    // specify loss-function and learning strategy
    network<sequential> nn;
    adagrad optimizer;

    construct_net(nn);

    std::cout << "load models..." << std::endl;

    // load training set and test set.
    std::vector<label_t> train_labels;
    std::vector<label_t> test_labels;
    std::vector<vec_t> train_images;
    std::vector<vec_t> test_images;

    load_dataset(train_labels, train_images, test_labels, test_images);

    std::cout << "start training: "<<train_images.size()<<" examples..."<< std::endl;

    progress_display disp(train_images.size());
    timer t;
    int minibatch_size = 100;
    int num_epochs = 50;

    // optimizer.alpha *= std::sqrt(minibatch_size);

    // create callback
    auto on_enumerate_epoch = [&](){
        std::cout << t.elapsed() << "s elapsed." << std::endl;
        tiny_cnn::result res = nn.test(test_images, test_labels);
        std::cout << res.num_success << "/" << res.num_total << std::endl;
        disp.restart(train_images.size());
        t.restart();
    };

    auto on_enumerate_minibatch = [&](){
        disp += minibatch_size;
    };

    // training
    nn.train<mse>(optimizer, train_images, train_labels, minibatch_size, num_epochs,
             on_enumerate_minibatch, on_enumerate_epoch);

    std::cout << "end training." << std::endl;

    // save networks
    std::ofstream ofs("weibo.cn-nn-weights");
    ofs << nn;
}
