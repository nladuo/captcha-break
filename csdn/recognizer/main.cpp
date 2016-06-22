#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <algorithm>
#include <map>
using namespace std;
using namespace cv;

void load_dataset(Mat dataset[])
{
    string dataset_dir = "../recognizer/dataset/";
    for(int i = 0; i < 6*10; i++){
        char buffer[255];
        sprintf(buffer, "%d", i/6);
        string image_path = dataset_dir + string(buffer);
        sprintf(buffer, "%d", i%6 + 1);
        image_path += string(buffer) + ".png";
        dataset[i] = imread(image_path, CV_LOAD_IMAGE_GRAYSCALE);
    }
}

void create_labels(int labels[])
{
    for(int i = 0; i < 6*10; i++){
        labels[i] = i/6;
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

int knn_classify(Mat letter, Mat dataset[],int labels[], int k)
{
    int distances[6*10];
    int sorted_distances[6*10];
    //count distances
    for(int i = 0; i < 6*10 ;i++){
        distances[i] = count_distance(letter, dataset[i]);
        sorted_distances[i] = distances[i];
    }
    sort(sorted_distances, sorted_distances+6*10);
    //get k_nearest array
    int* k_nearest = new int[k];
    for(int i = 0; i < k; i++){
        for(int j = 0; j < 6*10 ; j++){
            if(distances[j] == sorted_distances[i]){
                k_nearest[i] = labels[j];
                break;
            }
        }
    }
    // create a map which key is the label, and value is the label occurred count in k_nearest.
    map<int, int> labels_map;
    for(int i = 0; i < k; i++){
        if(labels_map.find(k_nearest[i]) == labels_map.end())
            labels_map[k_nearest[i]] = 0;
        else
            labels_map[k_nearest[i]]++;
    }
    //extract the max count of k_nearst
    int max_label = -1;
    labels_map[max_label] = -1;
    map<int,int>::iterator it;
    for(it=labels_map.begin();it!=labels_map.end();++it){
        if(it->second > labels_map[max_label]){
            max_label = it->first;
        }
    }
    delete[] k_nearest;
    return max_label;
}

void recognize(string path, Mat dataset[], int labels[])
{
    Mat test_image = imread(path, CV_LOAD_IMAGE_GRAYSCALE);
    threshold(test_image, test_image, 100, 255, cv::THRESH_BINARY);
    Range col_ranges[4] = {
        Range(5, 5+8),
        Range(14, 14+8),
        Range(23, 23+8),
        Range(32, 32+8)
    };
    cout<<"Result:";
    for(int i = 0; i < 4; i++){
        Mat letter = test_image.colRange(col_ranges[i]);
        cout << knn_classify(letter, dataset, labels, 5);
    }
    cout<<endl;
}

int main(int argc, char* argv[])
{
    if(argc != 2) {
        fprintf(stderr, "Usage: ./recognizer <image_filename>\n");
        return 1;
    }
    Mat dataset[10 * 6];
    int labels[10 * 6];
    load_dataset(dataset);
    create_labels(labels);
    recognize(argv[1], dataset, labels);

    return 0;
}
