#include "spliter.h"
#include <boost/filesystem.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

namespace fs = boost::filesystem;

int main(int argc, char *argv[])
{
    fs::path captchas_path("../downloader/captchas/");
    std::vector<std::string> images;

    //get all captcha files
    fs::directory_iterator end_iter;
    for (fs::directory_iterator iter(captchas_path); iter != end_iter; ++iter)
    {
        if (fs::extension(*iter)==".png")       
        {
            images.push_back(iter->path().string()); 
        }
    }

    //split all captchas
    std::vector<std::string>::iterator itr = images.begin();
    Spliter spliter("./dataset/");
    for (;itr != images.end(); ++itr)
    {
        std::cout<<*itr<<std::endl;
        spliter.split_and_save(*itr);

    }
    return 0;
}
